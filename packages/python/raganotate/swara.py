"""
swara.py — Swara & Swarasthana Definitions
===========================================
Carnatic music has 16 swarasthana NAMES but only 12 unique pitch POSITIONS.

The 12 chromatic positions use 5-limit Just Intonation (JI) ratios:
    S  r  R  g  G+  m  M  P  d  D  n  N+
    1  2  3  4   5  6  7  8  9 10 11  12

The 16 names arise from 4 enharmonic pairs — same frequency, different name
depending on raga context (arohana/avarohana):
    R2 (Chatusruti Ri)  =  G1 (Suddha Ga)      → symbol 'R',  ratio 9/8
    R3 (Shatshruti Ri)  =  G2 (Sadharana Ga)   → symbol 'g',  ratio 6/5
    D2 (Chatusruti Dha) =  N1 (Suddha Ni)      → symbol 'D',  ratio 5/3
    D3 (Shatshruti Dha) =  N2 (Kaisika Ni)     → symbol 'n',  ratio 9/5

In notation, G/G2 and N/N2 are accepted as aliases and resolve to 'g' and 'n'.

Ref: RagaNotate SPEC.md §4-5 · github.com/jags111/RagaNotate
     Sangita Sampradaya Pradarshini — Subbarama Dikshitar
     Melakartha 72-raga system (standard 5-limit JI)
"""

from fractions import Fraction
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Adhara Shadjam (tonic) — change to set a different Sa
DEFAULT_SA_HZ: float = 240.0

# Octave multipliers relative to Madhya Sthayi
OCTAVE_MULTIPLIER: dict[str, float] = {
    "mandra": 0.5,   # .s  lower octave  (½ × Sa)
    "madhya": 1.0,   # S   middle octave (1 × Sa)
    "tara":   2.0,   # S'  upper octave  (2 × Sa)
}

OCTAVE_PREFIXES: dict[str, str] = {
    "mandra": "LO",
    "madhya": "MD",
    "tara":   "HI",
}


# ---------------------------------------------------------------------------
# Swarasthana Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Swarasthana:
    """One of the 12 unique pitch positions in Carnatic music.

    Note: There are 16 swarasthana names but only 12 distinct frequencies.
    The 4 enharmonic pairs (R2=G1, R3=G2, D2=N1, D3=N2) share frequencies
    and are documented in ENHARMONIC_PAIRS below.
    """
    number:     int          # 1–12 (chromatic position)
    symbol:     str          # ASCII notation: S r R g G+ m M P d D n N+
    variant:    int          # 0=achala, 1=suddha, 2=chatusruti/prati, 3=shatsruti/antara/kakali
    name:       str          # Full Sanskrit name
    phonetic:   str          # Singable syllable: Sa Ra Ri Ga Gu Ma Mi Pa Da Dha Ni Nu
    token:      str          # AI token: SA_0, RI_1, RI_2, GA_2, GA_3 …
    ratio:      Fraction     # 5-limit JI ratio relative to Sa (madhya)
    swara_type: str          # "achala" (immovable) or "chala" (movable)

    def hz(self, octave: str = "madhya", sa_hz: float = DEFAULT_SA_HZ) -> float:
        """Return frequency in Hz for this swarasthana and octave."""
        return float(self.ratio) * sa_hz * OCTAVE_MULTIPLIER[octave]

    def ai_token(self, octave: str = "madhya") -> str:
        """Return full AI token with octave prefix, e.g. HI_RI_2."""
        return f"{OCTAVE_PREFIXES[octave]}_{self.token}"

    def __repr__(self) -> str:
        return (
            f"Swarasthana({self.symbol!r}, {self.name}, "
            f"ratio={self.ratio}, {float(self.ratio)*DEFAULT_SA_HZ:.2f}Hz)"
        )


# ---------------------------------------------------------------------------
# 12 Unique Pitch Positions  (5-limit Just Intonation)
# ---------------------------------------------------------------------------
#
#  Position  Symbol  Names                    Ratio   Hz@Sa=240  Cents
#  ────────  ──────  ──────────────────────── ──────  ─────────  ─────
#     1      S       Shadjam (achala)          1/1     240.00       0
#     2      r       R1 — Suddha Rishabha      16/15   256.00     112
#     3      R       R2 = G1                   9/8     270.00     204
#     4      g       R3 = G2 — Sadharana Ga    6/5     288.00     316
#     5      G+      G3 — Antara Gandhara      5/4     300.00     386
#     6      m       M1 — Suddha Madhyama      4/3     320.00     498
#     7      M       M2 — Prati Madhyama       45/32   337.50     590
#     8      P       Panchamam (achala)        3/2     360.00     702
#     9      d       D1 — Suddha Dhaivata      8/5     384.00     814
#    10      D       D2 = N1 — Chatusruti Dha  5/3     400.00     884
#    11      n       D3 = N2 — Shatshruti Dha  9/5     432.00     996
#    12      N+      N3 — Kakali Nishada       15/8    450.00    1088
#  ─────────────────────────────────────────────────────────────────────
#  Tara Sa   S'      Upper Shadjam             2/1     480.00    1200
#  Mandra Sa .s      Lower Shadjam             1/2     120.00   -1200

SWARASTHANAS: dict[str, Swarasthana] = {

    # ── Achala (immovable — never altered by raga) ─────────────────────────
    "S":  Swarasthana( 1, "S",   0, "Shadjam",
                       "Sa",  "SA_0",  Fraction(1,  1),  "achala"),

    "P":  Swarasthana( 8, "P",   0, "Panchamam",
                       "Pa",  "PA_0",  Fraction(3,  2),  "achala"),

    # ── Position 2: R1 only ────────────────────────────────────────────────
    "r":  Swarasthana( 2, "r",   1, "Suddha Rishabham (R1)",
                       "Ra",  "RI_1",  Fraction(16, 15), "chala"),

    # ── Position 3: R2 = G1 (enharmonic pair) ─────────────────────────────
    "R":  Swarasthana( 3, "R",   2, "Chatusruti Rishabham (R2) / Suddha Gandharam (G1)",
                       "Ri",  "RI_2",  Fraction(9,  8),  "chala"),

    # ── Position 4: R3 = G2 (enharmonic pair) ─────────────────────────────
    "g":  Swarasthana( 4, "g",   3, "Shatshruti Rishabham (R3) / Sadharana Gandharam (G2)",
                       "Ga",  "GA_2",  Fraction(6,  5),  "chala"),

    # ── Position 5: G3 only ────────────────────────────────────────────────
    "G+": Swarasthana( 5, "G+",  4, "Antara Gandharam (G3)",
                       "Gu",  "GA_3",  Fraction(5,  4),  "chala"),

    # ── Madhyamas ─────────────────────────────────────────────────────────
    "m":  Swarasthana( 6, "m",   1, "Suddha Madhyamam (M1)",
                       "Ma",  "MA_1",  Fraction(4,  3),  "chala"),

    "M":  Swarasthana( 7, "M",   2, "Prati Madhyamam (M2)",
                       "Mi",  "MA_2",  Fraction(45, 32), "chala"),

    # ── Position 9: D1 only ────────────────────────────────────────────────
    "d":  Swarasthana( 9, "d",   1, "Suddha Dhaivatam (D1)",
                       "Da",  "DA_1",  Fraction(8,  5),  "chala"),

    # ── Position 10: D2 = N1 (enharmonic pair) ────────────────────────────
    "D":  Swarasthana(10, "D",   2, "Chatusruti Dhaivatam (D2) / Suddha Nishadam (N1)",
                       "Dha", "DA_2",  Fraction(5,  3),  "chala"),

    # ── Position 11: D3 = N2 (enharmonic pair) ────────────────────────────
    "n":  Swarasthana(11, "n",   3, "Shatshruti Dhaivatam (D3) / Kaisika Nishadam (N2)",
                       "Ni",  "NI_2",  Fraction(9,  5),  "chala"),

    # ── Position 12: N3 only ──────────────────────────────────────────────
    "N+": Swarasthana(12, "N+",  4, "Kakali Nishadam (N3)",
                       "Nu",  "NI_3",  Fraction(15, 8),  "chala"),
}


# ---------------------------------------------------------------------------
# Variant aliases → canonical symbol
# ---------------------------------------------------------------------------
#
# Enharmonic truth table:
#   R2 = G1  →  symbol 'R'   (9/8 = 270 Hz)
#   R3 = G2  →  symbol 'g'   (6/5 = 288 Hz)
#   D2 = N1  →  symbol 'D'   (5/3 = 400 Hz)
#   D3 = N2  →  symbol 'n'   (9/5 = 432 Hz)
#
VARIANT_ALIAS: dict[str, str] = {
    # Rishabha variants
    "R1": "r",   # Suddha Ri
    "R2": "R",   # Chatusruti Ri  = G1
    "R3": "g",   # Shatshruti Ri  = G2

    # Gandhara variants (G1 and G2 share pitch with R2 and R3)
    "G1": "R",   # Suddha Ga      = R2 → same Hz as 'R'
    "G2": "g",   # Sadharana Ga   = R3 → same Hz as 'g'
    "G3": "G+",  # Antara Ga      (unique)

    # Backward-compat: 'G' in notation resolves to Sadharana Ga (G2 = R3)
    "G":  "g",

    # Madhyama variants
    "M1": "m",
    "M2": "M",

    # Dhaivata variants
    "D1": "d",   # Suddha Dha
    "D2": "D",   # Chatusruti Dha = N1
    "D3": "n",   # Shatshruti Dha = N2

    # Nishada variants (N1 and N2 share pitch with D2 and D3)
    "N1": "D",   # Suddha Ni      = D2 → same Hz as 'D'
    "N2": "n",   # Kaisika Ni     = D3 → same Hz as 'n'
    "N3": "N+",  # Kakali Ni      (unique)

    # Backward-compat: 'N' in notation resolves to Kaisika Ni (N2 = D3)
    "N":  "n",

    # Achala identity aliases
    "S":  "S",
    "P":  "P",

    # Octave-qualified forms
    "S'": "S",
    ".s": "S",
}


# ---------------------------------------------------------------------------
# Enharmonic Pairs  — same frequency, different name by raga context
# ---------------------------------------------------------------------------
#
# These 4 pairs are the reason there are 16 names but only 12 pitches.
# In raga grammar: the arohana may use the Ri name, avarohana the Ga name
# (e.g. Kharaharapriya: arohana uses R2, avarohana uses G2 = same pitch).
#
ENHARMONIC_PAIRS: list[tuple[str, str, str]] = [
    ("R",  "G1", "9/8  = 270.00 Hz — Chatusruti Ri ↔ Suddha Ga"),
    ("g",  "G2", "6/5  = 288.00 Hz — Shatshruti Ri / Sadharana Ga"),
    ("D",  "N1", "5/3  = 400.00 Hz — Chatusruti Dha ↔ Suddha Ni"),
    ("n",  "N2", "9/5  = 432.00 Hz — Shatshruti Dha / Kaisika Ni"),
]


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def resolve_symbol(sym: str) -> Optional[Swarasthana]:
    """Resolve a symbol (including variant aliases like G3, R2, N) to a Swarasthana.

    Args:
        sym: Swara symbol, e.g. "S", "R", "G3", "N+", "G", "N1"

    Returns:
        Swarasthana if found, else None.

    Examples:
        >>> resolve_symbol("G1")   # G1 = R2 → returns 'R' Swarasthana
        >>> resolve_symbol("N1")   # N1 = D2 → returns 'D' Swarasthana
        >>> resolve_symbol("G")    # G = G2 = R3 → returns 'g' Swarasthana
    """
    if sym in SWARASTHANAS:
        return SWARASTHANAS[sym]
    canonical = VARIANT_ALIAS.get(sym)
    if canonical and canonical in SWARASTHANAS:
        return SWARASTHANAS[canonical]
    return None


def swara_hz(
    symbol: str,
    octave: str = "madhya",
    sa_hz: float = DEFAULT_SA_HZ,
) -> float:
    """Return the frequency in Hz for a swara symbol.

    Args:
        symbol: Swara symbol, e.g. "S", "R", "G3", "N+", "G1"
        octave: "mandra" (×0.5), "madhya" (×1.0), or "tara" (×2.0)
        sa_hz:  Adhara Shadjam frequency in Hz (default 240.0)

    Returns:
        Frequency in Hz (5-limit Just Intonation)

    Raises:
        KeyError: if symbol is not recognized

    Examples:
        >>> swara_hz("G3", sa_hz=240.0)       # 300.0 Hz
        >>> swara_hz("G1", sa_hz=240.0)       # 270.0 Hz  (= R2)
        >>> swara_hz("N1", sa_hz=240.0)       # 400.0 Hz  (= D2)
        >>> swara_hz("N+", octave="tara", sa_hz=240.0)  # 900.0 Hz
    """
    sw = resolve_symbol(symbol)
    if sw is None:
        raise KeyError(
            f"Unknown swara symbol: {symbol!r}\n"
            f"  Valid symbols: {list(SWARASTHANAS.keys())}\n"
            f"  Valid aliases: {list(VARIANT_ALIAS.keys())}"
        )
    return float(sw.ratio) * sa_hz * OCTAVE_MULTIPLIER[octave]


def swara_ratio(symbol: str) -> Fraction:
    """Return the Just Intonation ratio for a swara symbol."""
    sw = resolve_symbol(symbol)
    if sw is None:
        raise KeyError(f"Unknown swara symbol: {symbol!r}")
    return sw.ratio


def print_scale(sa_hz: float = DEFAULT_SA_HZ) -> None:
    """Print all 12 swarasthana positions with frequencies for a given Sa."""
    sep = "─" * 78
    print(f"\n{sep}")
    print(f"  RagaNotate — 12-Position Swara Scale  (Sa = {sa_hz} Hz)")
    print(f"  12 unique pitches · 16 names (4 enharmonic pairs shown below)")
    print(f"{sep}")
    print(f"  {'#':3} {'Sym':5} {'Phonetic':8} {'Token':8} {'Ratio':8} {'Hz':>9}  Name")
    print(f"  {'─'*3} {'─'*5} {'─'*8} {'─'*8} {'─'*8} {'─'*9}  {'─'*42}")
    for sym, sw in SWARASTHANAS.items():
        hz = float(sw.ratio) * sa_hz
        alias = next(
            (f"= {b}" for a, b, _ in ENHARMONIC_PAIRS if a == sym),
            ""
        )
        print(
            f"  {sw.number:3} {sym:5} {sw.phonetic:8} {sw.token:8} "
            f"{str(sw.ratio):8} {hz:9.2f}  {sw.name} {alias}"
        )
    s2 = sa_hz * 2
    print(f"  {'─':3} {'S':5} {'Sa':8} {'SA_0':8} {'2/1':8} {s2:9.2f}  Tara Shadjam (upper octave)")
    print(f"\n  Enharmonic pairs (same Hz, different raga context):")
    for sym, alias, desc in ENHARMONIC_PAIRS:
        print(f"    '{sym}' ↔ {alias}: {desc}")
    print(f"{sep}\n")


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print_scale(240.0)
    print_scale(261.63)

    print("Enharmonic resolution examples:")
    for sym, expected_hz in [("G1", 270.0), ("G2", 288.0), ("N1", 400.0), ("N2", 432.0)]:
        hz = swara_hz(sym, sa_hz=240.0)
        canon = VARIANT_ALIAS.get(sym, sym)
        print(f"  {sym} → '{canon}' = {hz:.2f} Hz  (expected {expected_hz:.2f} Hz)  "
              f"{'✅' if abs(hz - expected_hz) < 0.01 else '✗'}")

    print("\nBackward-compat aliases:")
    for sym in ["G", "N"]:
        sw = resolve_symbol(sym)
        print(f"  '{sym}' → {sw}")
