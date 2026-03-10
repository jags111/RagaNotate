"""
parser.py — ASCII Notation String → Abstract Syntax Tree (AST)
===============================================================
Parses RagaNotate notation strings like:
    "| S R~ G M | P/D N S' | N\\D P | M G R S ||"

into a structured AST of SwaraNode, RestNode, BarNode, TalaNode.

Ref: RagaNotate SPEC.md · ARCHITECTURE.md · github.com/jags111/RagaNotate
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional

from .swara import resolve_symbol, Swarasthana, VARIANT_ALIAS
from .gamaka import parse_gamaka_symbol, Gamaka, GAMAKAS


# ---------------------------------------------------------------------------
# AST Node Types
# ---------------------------------------------------------------------------

@dataclass
class SwaraNode:
    """A single swara event in the notation."""
    symbol: str                         # Canonical symbol: S, R, G, G+…
    octave: str = "madhya"              # mandra / madhya / tara
    variant: int = 0                    # 0=default, 1/2/3 explicit
    duration: float = 1.0              # In aksharas
    gamaka: Optional[Gamaka] = None    # None = Ahata (direct)
    lyric: Optional[str] = None        # Syllable aligned to this swara
    raw: str = ""                       # Original token string

    @property
    def swarasthana(self) -> Optional[Swarasthana]:
        return resolve_symbol(self.symbol)

    def __repr__(self) -> str:
        gk = self.gamaka.symbol if self.gamaka else ""
        ly = f" [{self.lyric}]" if self.lyric else ""
        return f"SwaraNode({self.symbol}{gk}/{self.octave}/{self.duration}){ly}"


@dataclass
class RestNode:
    """A rest or silence in the notation."""
    duration: float = 1.0
    lyric: Optional[str] = None

    def __repr__(self) -> str:
        return f"RestNode({self.duration})"


@dataclass
class BarNode:
    """A bar (avartanam) separator `|`."""
    is_section_end: bool = False   # True for `||`

    def __repr__(self) -> str:
        return "BarNode(||)" if self.is_section_end else "BarNode(|)"


@dataclass
class HalfBeatNode:
    """A half-beat gap marker `,`."""
    def __repr__(self) -> str:
        return "HalfBeatNode"


@dataclass
class TalaNode:
    """Tala declaration at the start of a piece."""
    name: str
    jaati: str = "Chatusra"
    speed: str = "madhyama"  # prathama / madhyama / durita

    def __repr__(self) -> str:
        return f"TalaNode({self.name}, {self.jaati}, {self.speed})"


@dataclass
class LyricsNode:
    """A lyrics line aligned to notation."""
    syllables: list[str]

    def __repr__(self) -> str:
        return f"LyricsNode({self.syllables})"


# Union type for AST nodes
ASTNode = SwaraNode | RestNode | BarNode | HalfBeatNode | TalaNode | LyricsNode


@dataclass
class NotationAST:
    """The full parsed notation document."""
    tala: Optional[TalaNode] = None
    nodes: list[ASTNode] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def swaras(self) -> list[SwaraNode]:
        """Return only SwaraNode elements."""
        return [n for n in self.nodes if isinstance(n, SwaraNode)]

    def bars(self) -> list[list[ASTNode]]:
        """Split nodes into bar-separated groups."""
        bars: list[list[ASTNode]] = []
        current: list[ASTNode] = []
        for node in self.nodes:
            if isinstance(node, BarNode):
                if current:
                    bars.append(current)
                current = []
            else:
                current.append(node)
        if current:
            bars.append(current)
        return bars

    def __repr__(self) -> str:
        return f"NotationAST(tala={self.tala}, nodes={len(self.nodes)})"


# ---------------------------------------------------------------------------
# Lexer — tokenize notation string
# ---------------------------------------------------------------------------

# Regex patterns (order matters — longest match first)
_TALA_HDR   = re.compile(r"tala:\s*(\w+)", re.IGNORECASE)
_JAATI_HDR  = re.compile(r"jaati:\s*(\w+)", re.IGNORECASE)
_SPEED_HDR  = re.compile(r"speed:\s*(\w+)", re.IGNORECASE)
_SECTION_END = re.compile(r"\|\|")
_BAR        = re.compile(r"\|")
_HALF_BEAT  = re.compile(r",")
_REST       = re.compile(r"-")
_COMMENT    = re.compile(r"#[^\n]*")

# Swara token: optional leading-octave dot, swara letter(s), optional variant digit,
# optional gamaka suffix, optional duration marker
# Examples: S, R~, G3^, .g, S', N3\, P;, G2w, M1:
_SWARA_TOKEN = re.compile(
    r"(?P<octave_lo>\.)"           # mandra prefix
    r"?(?P<base>[SRGMPDNsrgmpdn])" # base swara letter
    r"(?P<upper>'|(?=[^'])|$)"      # tara suffix
    r"(?P<var>[+]?[123])?"          # variant: 1/2/3 or +
    r"(?P<dur>[;:]+)?"              # duration ; or :
    r"(?P<gmk>~~|~|/|\\|v|\^|w|vib|tr|gl|sp|nd|\*|\{[a-z]+\})?" # gamaka
)

# Simpler token-based tokenizer
_TOKEN_RE = re.compile(
    r"(?P<section_end>\|\|)"
    r"|(?P<bar>\|)"
    r"|(?P<half_beat>,)"
    r"|(?P<rest>-)"
    r"|(?P<comment>#[^\n]*)"
    r"|(?P<swara_raw>\.?[SRGMPDNsrgmpdn]['+]?[123]?[;:]*(?:~~|~|/|\\\\|v|\^|w|vib|tr|gl|sp|nd|\*|\{[a-z]+\})?)"
    r"|(?P<whitespace>\s+)"
)


# ---------------------------------------------------------------------------
# Swara Token Parser
# ---------------------------------------------------------------------------

def _parse_swara_token(raw: str) -> SwaraNode:
    """Parse a single swara token string into a SwaraNode.

    Examples:
        "S"     → S, madhya, dur=1, no gamaka
        "R~"    → R, madhya, dur=1, Kampita
        "G3^"   → G+, madhya, dur=1, Sphurita
        ".g"    → g, mandra, dur=1, no gamaka
        "S'"    → S, tara, dur=1, no gamaka
        "P;"    → P, madhya, dur=2, no gamaka
        "N3\\"  → N+, madhya, dur=1, Irakka Jaru
    """
    s = raw.strip()
    octave = "madhya"
    variant_suffix = ""
    duration = 1.0
    gamaka = None

    # 1. Mandra octave prefix
    if s.startswith("."):
        octave = "mandra"
        s = s[1:]

    # 2. Tara octave suffix (must check before removing)
    if s.endswith("'") or (len(s) > 1 and s[1] == "'"):
        octave = "tara"
        s = s.replace("'", "")

    # 3. Extract gamaka suffix (longest first)
    gamaka_suffixes = [
        "~~", "vib", "tr", "gl", "sp", "nd",
        "~", "/", "\\", "^", "v", "w", "*",
        "{or}", "{ot}", "{tr}", "{mu}", "{nm}", "{mx}", "{ul}",
    ]
    for gk_sym in gamaka_suffixes:
        if s.endswith(gk_sym):
            gamaka = parse_gamaka_symbol(gk_sym)
            s = s[: -len(gk_sym)]
            break

    # 4. Extract duration markers (trailing ; or :)
    dur_str = ""
    while s and s[-1] in ";:":
        dur_str = s[-1] + dur_str
        s = s[:-1]

    if dur_str:
        if dur_str == ";":
            duration = 2.0
        elif dur_str == ":":
            duration = 0.5
        elif dur_str == "::":
            duration = 0.25

    # 5. Extract variant digit
    variant = 0
    if s and s[-1] in "123":
        variant = int(s[-1])
        s = s[:-1]
    elif s.endswith("+"):
        variant = 3
        s = s[:-1]

    # 6. Build variant symbol
    base = s.upper() if s else "S"
    sym_key = f"{base}{variant}" if variant else base
    # Resolve through alias table
    resolved = VARIANT_ALIAS.get(sym_key, sym_key)

    return SwaraNode(
        symbol=resolved,
        octave=octave,
        variant=variant,
        duration=duration,
        gamaka=gamaka,
        raw=raw,
    )


# ---------------------------------------------------------------------------
# Main Parser
# ---------------------------------------------------------------------------

def parse_notation(
    notation: str,
    tala: str = "Adi",
    jaati: str = "Chatusra",
    speed: str = "madhyama",
) -> NotationAST:
    """Parse an ASCII notation string into a NotationAST.

    Args:
        notation: e.g. "| S R~ G M | P/D N S' ||"
        tala:     Tala name (default: "Adi")
        jaati:    Jaati name (default: "Chatusra")
        speed:    Speed (prathama/madhyama/durita)

    Returns:
        NotationAST with all parsed nodes.

    Example:
        ast = parse_notation("| S R~ G M | P/D N S' ||", tala="Adi")
        for sw in ast.swaras():
            print(sw)
    """
    ast = NotationAST(metadata={"tala": tala, "jaati": jaati, "speed": speed})

    # Parse optional header lines
    for line in notation.split("\n"):
        m = _TALA_HDR.search(line)
        if m:
            tala = m.group(1)
        m = _JAATI_HDR.search(line)
        if m:
            jaati = m.group(1)
        m = _SPEED_HDR.search(line)
        if m:
            speed = m.group(1)

    ast.tala = TalaNode(name=tala, jaati=jaati, speed=speed)

    # Tokenize
    for m in _TOKEN_RE.finditer(notation):
        kind = m.lastgroup
        val = m.group()

        if kind == "comment" or kind == "whitespace":
            continue
        elif kind == "section_end":
            ast.nodes.append(BarNode(is_section_end=True))
        elif kind == "bar":
            ast.nodes.append(BarNode())
        elif kind == "half_beat":
            ast.nodes.append(HalfBeatNode())
        elif kind == "rest":
            ast.nodes.append(RestNode())
        elif kind == "swara_raw":
            try:
                node = _parse_swara_token(val)
                ast.nodes.append(node)
            except Exception as e:
                # Skip unrecognized tokens gracefully
                pass

    return ast


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    example = "| S R~ G M | P/D N S' | N\\D P | M G R S ||"
    ast = parse_notation(example, tala="Adi")
    print(f"\nParsed: {ast}")
    print(f"\nTala: {ast.tala}")
    print(f"\nAll nodes:")
    for node in ast.nodes:
        print(f"  {node}")
    print(f"\nSwaras only ({len(ast.swaras())}):")
    for sw in ast.swaras():
        hz_info = ""
        if sw.swarasthana:
            from .swara import swara_hz
            hz = swara_hz(sw.symbol, sw.octave)
            hz_info = f"  @ {hz:.1f} Hz"
        print(f"  {sw}{hz_info}")
