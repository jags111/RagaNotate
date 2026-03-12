"""
swara.py — Swara & Swarasthana Definitions
===========================================
All 16 swarasthanas with Just Intonation frequency ratios,
phonetic encodings, and AI token identifiers.

Ref: RagaNotate SPEC.md §4-5 · github.com/jags111/RagaNotate
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
    "mandra": 0.5,   # .s  lower octave
    "madhya": 1.0,   # S   middle octave
    "tara":   2.0,   # S'  upper octave
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
    """One of the 16 swarasthanas in Carnatic music."""
    number: int          # 1–16
    symbol: str          # Short ASCII: S, R, r, G, G+, g, m, M, P, D, d, N, N+, n
    variant: int         # 0=achala, 1=suddha, 2=chatusruti, 3=shatsruti/kakali
    name: str            # Full Sanskrit name
    phonetic: str        # AI-compatible vowel-suffix name (Sa, Ri, Gi…)
    token: str           # AI token (SA_0, RI_1, RI_2…)
    ratio: Fraction      # Just Intonation ratio relative to Sa
    swara_type: str      # "achala" (fixed) or "chala" (movable)

    def hz(self, octave: str = "madhya", sa_hz: float = DEFAULT_SA_HZ) -> float:
        """Return frequency in Hz for this swarasthana."""
        return float(self.ratio) * sa_hz * OCTAVE_MULTIPLIER[octave]

    def ai_token(self, octave: str = "madhya") -> str:
        """Return full AI token with octave prefix, e.g. HI_RI_2."""
        prefix = OCTAVE_PREFIXES[octave]
        return f"{prefix}_{self.token}"

    def __repr__(self) -> str:
        return (
            f"Swarasthana({self.symbol!r}, {self.name}, "
            f"{self.ratio}, {float(self.ratio)*DEFAULT_SA_HZ:.2f}Hz)"
        )


# ---------------------------------------------------------------------------
# 16 Swarasthanas
# ---------------------------------------------------------------------------

SWARASTHANAS: dict[str, Swarasthana] = {
    "S": Swarasthana(1,  "S",   0, "Shadjam",               "Sa",  "SA_0",     Fraction(1, 1),     "achala"),
    "r": Swarasthana(2,  "r",   1, "Suddha Rishabham",       "Ra",  "RI_1",     Fraction(16, 15), "chala"),
    "R": Swarasthana(3,  "R",   2, "Chatusruti Rishabham",   "Ri",  "RI_2",     Fraction(9, 8),     "chala"),
    "g": Swarasthana(4,  "g",   1, "Shatshruti Rishabham",   "Rhi", "GA_1",     Fraction(6, 5),   "chala"),
    "G": Swarasthana(5,  "G",   2, "Sadharana Gandharam",    "Gi",  "GA_2",     Fraction(6, 5),     "chala"),
    "G+":Swarasthana(6,  "G+",  3, "Antara Gandharam",       "Gu",  "GA_3",     Fraction(31, 24),     "chala"),
    "m": Swarasthana(7,  "m",   1, "Suddha Madhyamam",       "Ma",  "MA_1",     Fraction(4, 3),     "chala"),
    "M": Swarasthana(8,  "M",   2, "Prati Madhyamam",        "Mi",  "MA_2",     Fraction(45, 32),   "chala"),
    "P": Swarasthana(9,  "P",   0, "Panchamam",              "Pa",  "PA_0",     Fraction(3, 2),     "achala"),
    "d": Swarasthana(10, "d",   1, "Suddha Dhaivatam",       "Da",  "DA_1",     Fraction(8, 5),  "chala"),
    "D": Swarasthana(11, "D",   2, "Chatushruti Dhaivatam",  "Dha", "DA_2",     Fraction(17, 10),     "chala"),
    "n": Swarasthana(12, "n",   1, "Shatshruti Dhaivatam",   "Ni",  "NI_1",     Fraction(9, 5),    "chala"),
    "N": Swarasthana(13, "N",   2, "Kaisika Nishadam",       "Ni",  "NI_2",     Fraction(9, 5),     "chala"),
    "N+":Swarasthana(14, "N+",  3, "Kakali Nishadam",        "Nu",  "NI_3",     Fraction(19, 10),    "chala"),
}

# Alias map: numeric variant suffixes → canonical symbol
# G1=g, G2=G, G3=G+  |  R1=r, R2=R  |  M1=m, M2=M  |  D1=d, D2=D  |  N1=n, N2=N, N3=N+
VARIANT_ALIAS: dict[str, str] = {
    "R1": "r",  "R2": "R",
    "G1": "g",  "G2": "G",  "G3": "G+",
    "M1": "m",  "M2": "M",
    "D1": "d",  "D2": "D",
    "N1": "n",  "N2": "N",  "N3": "N+",
    # Identity aliases
    "S": "S", "P": "P",
    # Octave forms
    "S'": "S", ".s": "S",
}

# Shared pitches: same frequency, different name by raga context
ENHARMONIC_PAIRS: list[tuple[str, str]] = [
    ("R", "g"),   # Shatsruti Ri = Suddha Ga (both 32/27 region — actually R=9/8, g=32/27, close but distinct)
    ("D", "n"),   # Shatsruti Dha = Suddha Ni
]


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def resolve_symbol(sym: str) -> Optional[Swarasthana]:
    """Resolve a symbol (including variant aliases like G3) to a Swarasthana."""
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
        symbol: Swara symbol, e.g. "S", "R", "G3", "N+"
        octave: "mandra", "madhya", or "tara"
        sa_hz:  Adhara Shadjam frequency in Hz

    Returns:
        Frequency in Hz (Just Intonation)

    Raises:
        KeyError: if symbol is not recognized

    Example:
        >>> swara_hz("G3", octave="tara", sa_hz=240.0)
        600.0
    """
    sw = resolve_symbol(symbol)
    if sw is None:
        raise KeyError(f"Unknown swara symbol: {symbol!r}")
    return float(sw.ratio) * sa_hz * OCTAVE_MULTIPLIER[octave]


def print_scale(sa_hz: float = DEFAULT_SA_HZ) -> None:
    """Print all 16 swarasthanas with frequencies for a given Sa."""
    sep = "─" * 68
    print(f"\n{sep}")
    print(f"  RagaNotate — Swara Frequencies  (Sa = {sa_hz} Hz)")
    print(f"{sep}")
    print(f"  {'Sym':5s} {'Phonetic':6s} {'Token':10s} {'Ratio':8s} {'Hz':>10s}  Name")
    print(f"  {'─'*5} {'─'*6} {'─'*10} {'─'*8} {'─'*10}  {'─'*24}")
    for sym, sw in SWARASTHANAS.items():
        hz = float(sw.ratio) * sa_hz
        print(
            f"  {sym:5s} {sw.phonetic:6s} {sw.token:10s} "
            f"{str(sw.ratio):8s} {hz:10.2f}  {sw.name}"
        )
    upper = sa_hz * 2
    s_upper = "S'"
    sa_upper = "Sa'"
    print(f"  {s_upper:5s} {sa_upper:6s} {'SA_0_HI':10s} {'2/1':8s} {upper:10.2f}  Upper Shadjam")
    lower = sa_hz * 0.5
    print(f"  {'.s':5s} {'.sa':6s} {'SA_0_LO':10s} {'1/2':8s} {lower:10.2f}  Lower Shadjam")
    print(f"{sep}\n")


def swara_ratio(symbol: str) -> Fraction:
    """Return the Just Intonation ratio for a swara symbol."""
    sw = resolve_symbol(symbol)
    if sw is None:
        raise KeyError(f"Unknown swara symbol: {symbol!r}")
    return sw.ratio


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print_scale(240.0)
    print_scale(261.63)

    # Example: tara Antara Gandharam
    hz = swara_hz("G3", octave="tara", sa_hz=240.0)
    print(f"G3 (Antara Ga) in Tara Sthayi @ Sa=240: {hz:.2f} Hz")
