"""
tala.py — Tala System (Suladi Sapta + Chapu + 108-Tala)
=========================================================
Defines all standard Carnatic talas, angas, and beat-clock utilities.

Ref: RagaNotate SPEC.md §8
     upbeatlabs.com · karnatik.com/ctaala · carnaticmusicexams.in
     github.com/jags111/RagaNotate
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator


# ---------------------------------------------------------------------------
# Anga Enum
# ---------------------------------------------------------------------------

class AngaType(str, Enum):
    ANUDHRUTAM = "U"    # 1 akshara  — downward palm clap
    DHRUTAM    = "O"    # 2 aksharas — palm-down + palm-up
    LAGHU      = "l"    # 3–9 aksharas (jaati-dependent)
    GURU       = "8"    # 8 aksharas
    PLUTAM     = ")"    # 12 aksharas
    KAKAPADAM  = "+"    # 16 aksharas


# Anga base aksharas (for non-Laghu angas)
ANGA_AKSHARAS: dict[AngaType, int] = {
    AngaType.ANUDHRUTAM: 1,
    AngaType.DHRUTAM:    2,
    AngaType.GURU:       8,
    AngaType.PLUTAM:     12,
    AngaType.KAKAPADAM:  16,
}


# ---------------------------------------------------------------------------
# Laghu Jaati
# ---------------------------------------------------------------------------

class Jaati(int, Enum):
    TISRA     = 3
    CHATUSRA  = 4
    KHANDA    = 5
    MISRA     = 7
    SANKEERNA = 9

JAATI_SOLKATTU: dict[Jaati, str] = {
    Jaati.TISRA:     "Tha Ki Ta",
    Jaati.CHATUSRA:  "Tha Ka Dhi Mi",
    Jaati.KHANDA:    "Tha Ka Tha Ki Ta",
    Jaati.MISRA:     "Tha Ki Ta Tha Ka Dhi Mi",
    Jaati.SANKEERNA: "Tha Ka Dhi Mi Tha Ka Tha Ki Ta",
}


# ---------------------------------------------------------------------------
# Anga Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Anga:
    """A single anga (component) in a tala."""
    anga_type: AngaType
    jaati: Jaati = Jaati.CHATUSRA  # only relevant for Laghu

    @property
    def aksharas(self) -> int:
        if self.anga_type == AngaType.LAGHU:
            return self.jaati.value
        return ANGA_AKSHARAS[self.anga_type]

    @property
    def symbol(self) -> str:
        if self.anga_type == AngaType.LAGHU:
            return f"l{self.jaati.value}"
        return self.anga_type.value

    def __repr__(self) -> str:
        return f"Anga({self.symbol}, {self.aksharas} aksharas)"


# ---------------------------------------------------------------------------
# Tala Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Tala:
    """A Carnatic tala definition."""
    name: str
    angas: list[Anga]
    description: str = ""

    @property
    def total_aksharas(self) -> int:
        return sum(a.aksharas for a in self.angas)

    @property
    def anga_symbols(self) -> list[str]:
        return [a.symbol for a in self.angas]

    def beat_pattern(self, bpm: float = 60.0) -> list[float]:
        """Return list of beat timestamps (seconds) for one avartanam.

        Args:
            bpm: Beats per minute (1 beat = 1 akshara)

        Returns:
            List of timestamps in seconds where each akshara falls.
        """
        beat_dur = 60.0 / bpm
        return [i * beat_dur for i in range(self.total_aksharas)]

    def __repr__(self) -> str:
        angas_str = " + ".join(self.anga_symbols)
        return f"Tala({self.name!r}, [{angas_str}], {self.total_aksharas} aksharas)"


# ---------------------------------------------------------------------------
# Suladi Sapta Talas (7 main talas × 5 jaatis = 35 talas)
# Default jaati: Chatusra
# ---------------------------------------------------------------------------

def _laghu(jaati: Jaati = Jaati.CHATUSRA) -> Anga:
    return Anga(AngaType.LAGHU, jaati)

def _dhrutam() -> Anga:
    return Anga(AngaType.DHRUTAM)

def _anudhrutam() -> Anga:
    return Anga(AngaType.ANUDHRUTAM)


TALAS: dict[str, Tala] = {

    # ── Dhruva Tala: l O l l = 14 aksharas (Chatusra) ──────────────────────
    "Dhruva": Tala(
        name="Dhruva",
        angas=[_laghu(), _dhrutam(), _laghu(), _laghu()],
        description="l O l l = 14 aksharas (Chatusra jaati)",
    ),

    # ── Matya Tala: l O l = 9 aksharas (Tisra) ─────────────────────────────
    "Matya": Tala(
        name="Matya",
        angas=[_laghu(Jaati.TISRA), _dhrutam(), _laghu(Jaati.TISRA)],
        description="l O l = 3+2+3 = 9 aksharas (Tisra jaati / 8 Chatusra)",
    ),

    # ── Rupaka Tala: O l = 6 aksharas ───────────────────────────────────────
    "Rupaka": Tala(
        name="Rupaka",
        angas=[_dhrutam(), _laghu()],
        description="O l = 2+4 = 6 aksharas — common in bhajans",
    ),

    # ── Jhampa Tala: l U O = 10 aksharas (Misra Laghu 7+1+2) ───────────────
    "Jhampa": Tala(
        name="Jhampa",
        angas=[_laghu(Jaati.MISRA), _anudhrutam(), _dhrutam()],
        description="l U O = 7+1+2 = 10 aksharas (Misra Laghu)",
    ),

    # ── Triputa Tala: l O O = 7 aksharas ────────────────────────────────────
    "Triputa": Tala(
        name="Triputa",
        angas=[_laghu(), _dhrutam(), _dhrutam()],
        description="l O O = 4+2+2 = 8 aksharas as Adi Tala (Chatusra Laghu)",
    ),

    # ── Ata Tala: l l O O = 14 aksharas ─────────────────────────────────────
    "Ata": Tala(
        name="Ata",
        angas=[_laghu(), _laghu(), _dhrutam(), _dhrutam()],
        description="l l O O = 4+4+2+2 = 14 aksharas",
    ),

    # ── Eka Tala: l = 4 aksharas ─────────────────────────────────────────────
    "Eka": Tala(
        name="Eka",
        angas=[_laghu()],
        description="Single Laghu = 4 aksharas",
    ),
}

# Adi Tala = Chatusra Jati Triputa (most common, 8 beats)
TALAS["Adi"] = Tala(
    name="Adi",
    angas=[_laghu(Jaati.CHATUSRA), _dhrutam(), _dhrutam()],
    description="Chatusra Jati Triputa = l4 O O = 4+2+2 = 8 aksharas (most common)",
)


# ---------------------------------------------------------------------------
# Chapu Talas
# ---------------------------------------------------------------------------

CHAPU_TALAS: dict[str, dict] = {
    "Thisra_Chapu":    {"beats": 3, "pattern": "1+2", "solkattu": "Tha-Ki-Ta"},
    "Khanda_Chapu":    {"beats": 5, "pattern": "2+3", "solkattu": "Tha-Ka-Tha-Ki-Ta"},
    "Misra_Chapu":     {"beats": 7, "pattern": "3+4", "solkattu": "Tha-Ki-Ta-Tha-Ka-Dhi-Mi"},
    "Sankeerna_Chapu": {"beats": 9, "pattern": "4+5", "solkattu": "Tha-Ka-Dhi-Mi-Tha-Ka-Tha-Ki-Ta"},
}


# ---------------------------------------------------------------------------
# TalaEngine — beat clock
# ---------------------------------------------------------------------------

class TalaEngine:
    """Generates beat timestamps and anga markers for a given tala + BPM."""

    def __init__(self, tala: Tala, bpm: float = 60.0):
        self.tala = tala
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm   # seconds per akshara

    @property
    def avartanam_duration(self) -> float:
        """Duration of one full cycle (avartanam) in seconds."""
        return self.tala.total_aksharas * self.beat_duration

    def beats(self) -> Iterator[dict]:
        """Yield beat info dicts for one avartanam.

        Yields:
            dict with keys: akshara, time_s, anga, anga_beat, is_anga_start
        """
        akshara = 0
        for anga_idx, anga in enumerate(self.tala.angas):
            for beat_in_anga in range(anga.aksharas):
                yield {
                    "akshara":      akshara,
                    "time_s":       akshara * self.beat_duration,
                    "anga":         anga,
                    "anga_index":   anga_idx,
                    "beat_in_anga": beat_in_anga,
                    "is_anga_start": beat_in_anga == 0,
                }
                akshara += 1

    def print_beatmap(self) -> None:
        """Print a visual beatmap for this tala."""
        sep = "─" * 60
        print(f"\n{sep}")
        print(f"  {self.tala.name} Tala — {self.tala.total_aksharas} aksharas @ {self.bpm} BPM")
        print(f"  Angas: {' '.join(self.tala.anga_symbols)}")
        print(f"{sep}")
        print(f"  {'Beat':>5}  {'Time(s)':>8}  {'Anga':>6}  {'Anga Beat':>10}  {'Marker'}")
        print(f"  {'─'*5}  {'─'*8}  {'─'*6}  {'─'*10}  {'─'*10}")
        for b in self.beats():
            marker = "▶ " if b["is_anga_start"] else "  "
            print(
                f"  {b['akshara']+1:>5}  {b['time_s']:>8.3f}  "
                f"{b['anga'].symbol:>6}  {b['beat_in_anga']+1:>10}  {marker}"
            )
        print(f"{sep}\n")


# ---------------------------------------------------------------------------
# Lookup helper
# ---------------------------------------------------------------------------

def get_tala(name: str) -> Tala:
    """Return a Tala by name (case-insensitive).

    Raises:
        KeyError if not found.
    """
    for k, v in TALAS.items():
        if k.lower() == name.lower():
            return v
    raise KeyError(f"Unknown tala: {name!r}. Available: {list(TALAS.keys())}")


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Suladi Sapta Talas:\n")
    for name, tala in TALAS.items():
        print(f"  {name:12s}  {' '.join(tala.anga_symbols):16s}  {tala.total_aksharas:3d} aksharas")

    print("\nChapu Talas:\n")
    for name, info in CHAPU_TALAS.items():
        print(f"  {name:20s}  {info['beats']} beats  {info['pattern']}")

    # Beat clock demo
    engine = TalaEngine(TALAS["Adi"], bpm=80.0)
    engine.print_beatmap()
