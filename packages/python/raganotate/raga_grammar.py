"""
raga_grammar.py — Raga Definitions & Swara Validation
======================================================
Defines raga arohana/avarohana scales, vadi/samvadi swaras,
and idiomatic gamaka rules for each raga.

Ref: ragasangrah.com · karnatik.com · github.com/jags111/RagaNotate
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Raga Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Raga:
    """A Carnatic raga definition."""
    name: str
    arohana: list[str]          # Ascending scale (swara symbols)
    avarohana: list[str]        # Descending scale (swara symbols)
    vadi: str                   # Principal swara
    samvadi: str                # Secondary swara
    gamaka_rules: dict[str, list[str]] = field(default_factory=dict)
    # gamaka_rules: {swara_symbol: [preferred GMK tokens]}
    description: str = ""
    melakarta: Optional[int] = None   # Melakarta number (if janya raga)

    @property
    def allowed_swaras(self) -> set[str]:
        """All unique swaras permitted in this raga."""
        return set(self.arohana) | set(self.avarohana) - {"S", "P", "S'"}

    def is_valid_ascent(self, swaras: list[str]) -> bool:
        """Check if a sequence is valid in arohana (loose check)."""
        allowed = set(self.arohana)
        return all(s in allowed for s in swaras)

    def is_valid_descent(self, swaras: list[str]) -> bool:
        """Check if a sequence is valid in avarohana (loose check)."""
        allowed = set(self.avarohana)
        return all(s in allowed for s in swaras)

    def preferred_gamakas(self, swara: str) -> list[str]:
        """Return preferred gamaka tokens for a swara in this raga."""
        return self.gamaka_rules.get(swara, ["GMK_AHAT"])

    def __repr__(self) -> str:
        aro = " ".join(self.arohana)
        ava = " ".join(self.avarohana)
        return f"Raga({self.name!r}\n  aro: {aro}\n  ava: {ava}\n)"


# ---------------------------------------------------------------------------
# Raga Definitions
# ---------------------------------------------------------------------------

RAGAS: dict[str, Raga] = {

    # ── Hamsadhvani (Pentatonic — S R G3 P N3) ──────────────────────────────
    "Hamsadhvani": Raga(
        name="Hamsadhvani",
        arohana=  ["S", "R", "G+", "P", "N+", "S'"],
        avarohana=["S'", "N+", "P", "G+", "R", "S"],
        vadi="G+", samvadi="N+",
        gamaka_rules={
            "G+": ["GMK_KAMP", "GMK_SPHU"],
            "N+": ["GMK_KAMP", "GMK_IJRU"],
            "R":  ["GMK_EJRU"],
            "P":  ["GMK_AHAT"],
        },
        description="Pentatonic raga — S R G3 P N3. Joyful, auspicious.",
    ),

    # ── Shankarabharanam (72nd Melakarta — Bilaval thaat) ───────────────────
    "Shankarabharanam": Raga(
        name="Shankarabharanam",
        arohana=  ["S", "R", "G+", "m", "P", "D", "N+", "S'"],
        avarohana=["S'", "N+", "D", "P", "m", "G+", "R", "S"],
        vadi="G+", samvadi="N+",
        gamaka_rules={
            "G+": ["GMK_KAMP"],
            "N+": ["GMK_KAMP", "GMK_IJRU"],
            "D":  ["GMK_KAMP", "GMK_SPHU"],
            "m":  ["GMK_EJRU", "GMK_KAMP"],
        },
        description="Major scale equivalent. 29th Melakarta.",
        melakarta=29,
    ),

    # ── Kalyani (Yaman in Hindustani) ────────────────────────────────────────
    "Kalyani": Raga(
        name="Kalyani",
        arohana=  ["S", "R", "G+", "M", "P", "D", "N+", "S'"],
        avarohana=["S'", "N+", "D", "P", "M", "G+", "R", "S"],
        vadi="M", samvadi="S",
        gamaka_rules={
            "G+": ["GMK_KAMP"],
            "M":  ["GMK_KAMP", "GMK_EJRU"],
            "N+": ["GMK_KAMP"],
            "D":  ["GMK_SPHU"],
        },
        description="Prati Madhyamam (tritone). Evening raga.",
        melakarta=65,
    ),

    # ── Bhairavi (Hindustani Bhairavi / Carnatic Sindhu Bhairavi) ───────────
    "Bhairavi": Raga(
        name="Bhairavi",
        arohana=  ["S", "r", "G", "m", "P", "d", "N", "S'"],
        avarohana=["S'", "N", "d", "P", "m", "G", "r", "S"],
        vadi="m", samvadi="S",
        gamaka_rules={
            "G": ["GMK_KAMP", "GMK_ANDO"],
            "N": ["GMK_IJRU", "GMK_KAMP"],
            "r": ["GMK_EJRU"],
        },
        description="Melancholic, expressive. Morning raga.",
    ),

    # ── Mohanam (Bhupali in Hindustani) ─────────────────────────────────────
    "Mohanam": Raga(
        name="Mohanam",
        arohana=  ["S", "R", "G+", "P", "D", "S'"],
        avarohana=["S'", "D", "P", "G+", "R", "S"],
        vadi="G+", samvadi="D",
        gamaka_rules={
            "G+": ["GMK_KAMP", "GMK_EJRU"],
            "D":  ["GMK_KAMP"],
            "R":  ["GMK_SPHU"],
        },
        description="Pentatonic — S R G3 P D2. Sweet, popular.",
    ),

    # ── Bilahari ─────────────────────────────────────────────────────────────
    "Bilahari": Raga(
        name="Bilahari",
        arohana=  ["S", "R", "G+", "P", "D", "S'"],
        avarohana=["S'", "N+", "D", "P", "m", "G+", "R", "S"],
        vadi="G+", samvadi="D",
        gamaka_rules={
            "G+": ["GMK_KAMP"],
            "D":  ["GMK_KAMP", "GMK_EJRU"],
            "N+": ["GMK_IJRU"],
        },
        description="Asymmetric — pentatonic ascent, heptatonic descent.",
    ),

    # ── Todi ─────────────────────────────────────────────────────────────────
    "Todi": Raga(
        name="Todi",
        arohana=  ["S", "r", "G", "M", "P", "d", "N+", "S'"],
        avarohana=["S'", "N+", "d", "P", "M", "G", "r", "S"],
        vadi="M", samvadi="S",
        gamaka_rules={
            "G":  ["GMK_ANDO", "GMK_KAMP"],
            "M":  ["GMK_KAMP"],
            "d":  ["GMK_ANDO"],
            "N+": ["GMK_KAMP", "GMK_IJRU"],
        },
        description="Prati Madhyamam + flat notes. Serious, contemplative.",
        melakarta=45,
    ),

    # ── Kharaharapriya ───────────────────────────────────────────────────────
    "Kharaharapriya": Raga(
        name="Kharaharapriya",
        arohana=  ["S", "R", "G", "m", "P", "D", "N", "S'"],
        avarohana=["S'", "N", "D", "P", "m", "G", "R", "S"],
        vadi="G", samvadi="N",
        gamaka_rules={
            "G": ["GMK_KAMP"],
            "N": ["GMK_KAMP", "GMK_IJRU"],
        },
        description="Dorian mode equivalent. 22nd Melakarta.",
        melakarta=22,
    ),
}


# ---------------------------------------------------------------------------
# Lookup helper
# ---------------------------------------------------------------------------

def get_raga(name: str) -> Raga:
    """Return a Raga by name (case-insensitive).

    Raises:
        KeyError if not found.
    """
    for k, v in RAGAS.items():
        if k.lower() == name.lower():
            return v
    raise KeyError(f"Unknown raga: {name!r}. Available: {list(RAGAS.keys())}")


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for name, raga in RAGAS.items():
        aro = " ".join(raga.arohana)
        ava = " ".join(raga.avarohana)
        print(f"\n{name}")
        print(f"  Arohana:  {aro}")
        print(f"  Avarohana:{ava}")
        print(f"  Vadi: {raga.vadi}  Samvadi: {raga.samvadi}")
