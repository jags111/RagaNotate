"""
ai_encoder.py — Notation → AI Token Sequences for LLM Training
================================================================
Converts a NotationAST into various AI-ready representations:

  1. Token sequence    — flat list of string tokens for LLM tokenization
  2. Feature matrix   — numpy array of per-swara feature vectors
  3. JSON dataset     — serializable dict for HuggingFace datasets
  4. Phonetic string  — human-readable phonetic syllable sequence

Token vocabulary design follows iSargam (Springer 2016) conventions,
extended with RagaNotate gamaka and tala tokens.

Ref: ARCHITECTURE.md
     iSargam: https://link.springer.com/article/10.1186/s13636-016-0083-z
     github.com/jags111/RagaNotate
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import json

from .parser import NotationAST, SwaraNode, RestNode, BarNode
from .swara import swara_hz, SWARASTHANAS, DEFAULT_SA_HZ, OCTAVE_MULTIPLIER
from .gamaka import GAMAKAS, PitchCurveType
from .tala import get_tala


# ---------------------------------------------------------------------------
# Special tokens
# ---------------------------------------------------------------------------

SPECIAL_TOKENS = {
    # Structure
    "PAD":     "[PAD]",
    "UNK":     "[UNK]",
    "BOS":     "[BOS]",    # Beginning of sequence
    "EOS":     "[EOS]",    # End of sequence
    "BAR":     "[BAR]",    # Bar line |
    "SBAR":    "[SBAR]",   # Section end ||
    "HALF":    "[HALF]",   # Half-beat ,
    "REST":    "[REST]",   # Silence -
    # Octave tags
    "OCT_LO":  "[LO]",
    "OCT_MD":  "[MD]",
    "OCT_HI":  "[HI]",
    # Tala tags
    "TALA_START": "[TALA:",
    "TALA_END":   "]",
}

OCTAVE_TAG = {
    "mandra": "[LO]",
    "madhya": "[MD]",
    "tara":   "[HI]",
}


# ---------------------------------------------------------------------------
# Token builder
# ---------------------------------------------------------------------------

def swara_to_token(sw: SwaraNode) -> str:
    """Convert a SwaraNode to a single AI token string.

    Format: {OCTAVE_TAG}{SWARA_TOKEN}:{GAMAKA_TOKEN}
    Examples:
        [MD]RI_2:GMK_KAMP
        [HI]SA_0:GMK_AHAT
        [LO]GA_2:GMK_ANDO
    """
    # Octave prefix
    oct_tag = OCTAVE_TAG[sw.octave]

    # Swara token
    sw_def = SWARASTHANAS.get(sw.symbol)
    sw_token = sw_def.token if sw_def else "UNK"

    # Gamaka token
    gk_token = sw.gamaka.token if sw.gamaka else "GMK_AHAT"

    return f"{oct_tag}{sw_token}:{gk_token}"


def ast_to_token_sequence(
    ast: NotationAST,
    include_bos_eos: bool = True,
    include_tala: bool = True,
) -> list[str]:
    """Convert a full NotationAST to a flat token sequence.

    Args:
        ast:            Parsed notation
        include_bos_eos: Wrap with [BOS] … [EOS] tokens
        include_tala:   Prepend tala declaration token

    Returns:
        List of string tokens ready for tokenizer encoding.

    Example:
        tokens = ast_to_token_sequence(ast)
        # → ['[BOS]', '[TALA:Adi]', '[BAR]', '[MD]SA_0:GMK_AHAT', ...]
    """
    tokens: list[str] = []

    if include_bos_eos:
        tokens.append(SPECIAL_TOKENS["BOS"])

    if include_tala and ast.tala:
        tokens.append(f"[TALA:{ast.tala.name}]")

    for node in ast.nodes:
        if isinstance(node, BarNode):
            tokens.append(SPECIAL_TOKENS["SBAR"] if node.is_section_end else SPECIAL_TOKENS["BAR"])

        elif isinstance(node, RestNode):
            # Encode rest with duration
            if node.duration == 1.0:
                tokens.append(SPECIAL_TOKENS["REST"])
            else:
                tokens.append(f"[REST:{node.duration}]")

        elif isinstance(node, SwaraNode):
            tok = swara_to_token(node)
            # Add duration suffix if not 1.0
            if node.duration != 1.0:
                tok += f":{node.duration}"
            tokens.append(tok)
            # Append lyric token if present
            if node.lyric:
                tokens.append(f"[LYR:{node.lyric}]")

    if include_bos_eos:
        tokens.append(SPECIAL_TOKENS["EOS"])

    return tokens


# ---------------------------------------------------------------------------
# Feature Matrix
# ---------------------------------------------------------------------------

@dataclass
class SwaraFeature:
    """A per-swara feature vector for ML training."""
    # Pitch
    hz: float                   # Absolute frequency in Hz
    ratio_num: int              # JI ratio numerator
    ratio_den: int              # JI ratio denominator
    octave_id: int              # 0=mandra, 1=madhya, 2=tara
    swara_id: int               # 0–13 (position in 14-swara set)
    # Duration
    duration: float             # Aksharas
    # Gamaka
    gamaka_id: int              # 0–14 (gamaka index)
    curve_type: int             # 0–9 (PitchCurveType)
    gamaka_intensity: float     # 0.0–1.0
    gamaka_rate: float          # Hz (oscillation rate)
    # Raga/tala context
    bar_position: float         # 0.0–1.0 (normalized position in bar)
    tala_aksharas: int          # Total aksharas in tala cycle

    def to_list(self) -> list[float]:
        """Return feature as a flat float list for numpy."""
        return [
            self.hz, float(self.ratio_num), float(self.ratio_den),
            float(self.octave_id), float(self.swara_id),
            self.duration,
            float(self.gamaka_id), float(self.curve_type),
            self.gamaka_intensity, self.gamaka_rate,
            self.bar_position, float(self.tala_aksharas),
        ]


SWARA_ID_MAP = {sym: i for i, sym in enumerate(SWARASTHANAS.keys())}
OCTAVE_ID_MAP = {"mandra": 0, "madhya": 1, "tara": 2}
GAMAKA_ID_MAP = {tok: i for i, tok in enumerate(GAMAKAS.keys())}


def ast_to_feature_matrix(
    ast: NotationAST,
    sa_hz: float = DEFAULT_SA_HZ,
) -> list[SwaraFeature]:
    """Convert AST to a list of per-swara feature vectors.

    Args:
        ast:   Parsed notation AST
        sa_hz: Adhara Shadjam frequency

    Returns:
        List of SwaraFeature objects (one per swara node).
    """
    features: list[SwaraFeature] = []

    tala_aksharas = 8  # default Adi
    if ast.tala:
        try:
            t = get_tala(ast.tala.name)
            tala_aksharas = t.total_aksharas
        except KeyError:
            pass

    bar_notes: list[SwaraNode] = []
    all_bars: list[list[SwaraNode]] = []
    for node in ast.nodes:
        if isinstance(node, BarNode):
            if bar_notes:
                all_bars.append(bar_notes)
            bar_notes = []
        elif isinstance(node, SwaraNode):
            bar_notes.append(node)
    if bar_notes:
        all_bars.append(bar_notes)

    for bar in all_bars:
        total_dur = sum(sw.duration for sw in bar)
        cum_dur = 0.0
        for sw in bar:
            hz = swara_hz(sw.symbol, sw.octave, sa_hz)
            sw_def = SWARASTHANAS.get(sw.symbol)
            ratio_num = int(sw_def.ratio.numerator) if sw_def else 1
            ratio_den = int(sw_def.ratio.denominator) if sw_def else 1

            gmk = sw.gamaka
            gmk_token = gmk.token if gmk else "GMK_AHAT"
            gmk_id = GAMAKA_ID_MAP.get(gmk_token, 13)  # 13 = GMK_AHAT index
            curve = int(gmk.curve_type) if gmk else 0
            intensity = gmk.default_intensity if gmk else 1.0
            rate = gmk.default_rate if gmk else 0.0

            features.append(SwaraFeature(
                hz=hz,
                ratio_num=ratio_num,
                ratio_den=ratio_den,
                octave_id=OCTAVE_ID_MAP.get(sw.octave, 1),
                swara_id=SWARA_ID_MAP.get(sw.symbol, 0),
                duration=sw.duration,
                gamaka_id=gmk_id,
                curve_type=curve,
                gamaka_intensity=intensity,
                gamaka_rate=rate,
                bar_position=cum_dur / max(total_dur, 1.0),
                tala_aksharas=tala_aksharas,
            ))
            cum_dur += sw.duration

    return features


# ---------------------------------------------------------------------------
# JSON Dataset Record
# ---------------------------------------------------------------------------

def ast_to_dataset_record(
    ast: NotationAST,
    sa_hz: float = DEFAULT_SA_HZ,
    composition_id: str = "",
    raga: str = "",
    source: str = "",
) -> dict:
    """Serialize a NotationAST to a HuggingFace-compatible dataset record.

    Args:
        ast:            Parsed notation
        sa_hz:          Tonic frequency
        composition_id: Unique identifier string
        raga:           Raga name
        source:         Source reference

    Returns:
        Dict with keys: id, raga, tala, sa_hz, tokens, features, swaras
    """
    tokens = ast_to_token_sequence(ast)
    features = ast_to_feature_matrix(ast, sa_hz)

    swaras = []
    for sw in ast.swaras():
        hz = swara_hz(sw.symbol, sw.octave, sa_hz)
        swaras.append({
            "symbol":   sw.symbol,
            "octave":   sw.octave,
            "duration": sw.duration,
            "gamaka":   sw.gamaka.token if sw.gamaka else "GMK_AHAT",
            "lyric":    sw.lyric,
            "hz":       round(hz, 2),
        })

    return {
        "id":       composition_id,
        "raga":     raga,
        "tala":     ast.tala.name if ast.tala else "",
        "sa_hz":    sa_hz,
        "source":   source,
        "tokens":   tokens,
        "token_count": len(tokens),
        "features": [f.to_list() for f in features],
        "swaras":   swaras,
        "metadata": ast.metadata,
    }


# ---------------------------------------------------------------------------
# Phonetic String
# ---------------------------------------------------------------------------

def ast_to_phonetic(ast: NotationAST) -> str:
    """Convert AST to a human-readable phonetic syllable string.

    Example:
        "Sa Ri Gi Ma | Pa Di Ni Sa' | ..."

    Useful for pronunciation guides and TTS input.
    """
    parts: list[str] = []
    for node in ast.nodes:
        if isinstance(node, BarNode):
            parts.append("||" if node.is_section_end else "|")
        elif isinstance(node, RestNode):
            parts.append("-")
        elif isinstance(node, SwaraNode):
            sw_def = SWARASTHANAS.get(node.symbol)
            phonetic = sw_def.phonetic if sw_def else node.symbol
            if node.octave == "tara":
                phonetic += "'"
            elif node.octave == "mandra":
                phonetic = "." + phonetic.lower()
            parts.append(phonetic)
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Vocabulary builder (for tokenizer training)
# ---------------------------------------------------------------------------

def build_vocabulary() -> list[str]:
    """Return the full RagaNotate token vocabulary.

    Use this to initialize a custom tokenizer for LLM fine-tuning.

    Returns:
        Sorted list of all possible token strings.
    """
    vocab: set[str] = set()

    # Special tokens
    vocab.update(SPECIAL_TOKENS.values())
    vocab.add("[BOS]")
    vocab.add("[EOS]")

    # Tala tokens
    from .tala import TALAS, CHAPU_TALAS
    for name in list(TALAS.keys()) + list(CHAPU_TALAS.keys()):
        vocab.add(f"[TALA:{name}]")

    # Swara × octave × gamaka tokens
    octave_tags = ["[LO]", "[MD]", "[HI]"]
    durations = [1.0, 2.0, 0.5, 0.25]
    for sw_def in SWARASTHANAS.values():
        for oct_tag in octave_tags:
            for gk_token in GAMAKAS.keys():
                base = f"{oct_tag}{sw_def.token}:{gk_token}"
                vocab.add(base)
                for dur in durations:
                    if dur != 1.0:
                        vocab.add(f"{base}:{dur}")

    # Rest with durations
    for dur in durations:
        vocab.add(f"[REST:{dur}]")

    return sorted(vocab)


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from .parser import parse_notation
    from .lyrics_mapper import align_lyrics_to_notation

    lyrics   = "Va-tha-pi Ga-na-pa-tim Bha-je"
    notation = "| S R G P | N S' N P | G R S |"
    ast = align_lyrics_to_notation(lyrics, notation, tala="Adi", raga="Hamsadhvani")

    print("\n── Token Sequence ─────────────────────────────────────────")
    tokens = ast_to_token_sequence(ast)
    print(f"  Total tokens: {len(tokens)}")
    for i, tok in enumerate(tokens):
        print(f"  [{i:02d}] {tok}")

    print("\n── Feature Matrix ─────────────────────────────────────────")
    features = ast_to_feature_matrix(ast)
    print(f"  Total feature vectors: {len(features)}")
    print(f"  Feature dimensions:    {len(features[0].to_list())}")
    for i, f in enumerate(features[:4]):
        print(f"  [{i}] hz={f.hz:.1f}  swara_id={f.swara_id}  gamaka_id={f.gamaka_id}  pos={f.bar_position:.2f}")
    print("  ...")

    print("\n── Phonetic String ────────────────────────────────────────")
    print(" ", ast_to_phonetic(ast))

    print("\n── Dataset Record (preview) ───────────────────────────────")
    record = ast_to_dataset_record(
        ast, sa_hz=240.0,
        composition_id="vathapi_001",
        raga="Hamsadhvani",
        source="Traditional composition — Muthuswami Dikshitar",
    )
    preview = {k: v for k, v in record.items() if k not in ("features", "tokens")}
    print(json.dumps(preview, indent=2))

    print(f"\n── Vocabulary Size ────────────────────────────────────────")
    vocab = build_vocabulary()
    print(f"  {len(vocab)} tokens")
    print("  Sample:", vocab[:5], "...", vocab[-5:])
