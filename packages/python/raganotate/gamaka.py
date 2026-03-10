"""
gamaka.py — Gamaka Definitions, Symbols & AI Feature Vectors
=============================================================
The 15 classical gamakas of Carnatic music, with:
  - ASCII notation symbols (RagaNotate spec)
  - AI token identifiers
  - 6-dimensional ML feature vectors
  - Pitch contour functions for audio synthesis

Ref: RagaNotate SPEC.md §7 · Natya Shastra · Sangita Sampradaya Pradarshini
     github.com/jags111/RagaNotate
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
import math


# ---------------------------------------------------------------------------
# Pitch Curve Type Enum
# ---------------------------------------------------------------------------

class PitchCurveType(int, Enum):
    FLAT           = 0   # Ahata — direct, no ornament
    LINEAR_UP      = 1   # Etra Jaru — ascending slide
    LINEAR_DOWN    = 2   # Irakka Jaru — descending slide
    OSCILLATE      = 3   # Kampita — vibrato-like
    WIDE_OSCILLATE = 4   # Andola — slow wide oscillation
    GRACE_UP       = 5   # Sphurita — grace note above → target
    GRACE_DOWN     = 6   # Pratyaghata — grace note below → target
    ACCENT         = 7   # Nokku — stress accent
    FADE           = 8   # Namita — decreasing volume
    COMPLEX        = 9   # Misrita / Ullasita / Orikkai — complex


# ---------------------------------------------------------------------------
# Gamaka Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Gamaka:
    """A single Carnatic gamaka ornament."""
    token: str                  # AI token: GMK_KAMP, GMK_EJRU…
    symbol: str                 # ASCII notation symbol: ~ / \ ^ v w tr gl
    name: str                   # English name
    sanskrit: str               # Sanskrit / Tamil name
    description: str            # Brief description
    curve_type: PitchCurveType  # Pitch contour type (0–9)
    phonetic: str               # Pronunciation guide
    # Default ML feature vector defaults (intensity, rate)
    default_intensity: float = 0.5
    default_rate: float = 5.0    # Hz for oscillation-type gamakas

    def feature_vector(
        self,
        onset_hz: float,
        target_hz: float,
        duration_beats: float,
        intensity: float | None = None,
        raga_context: int = 0,
    ) -> list[float]:
        """Return 6-dimensional ML feature vector.

        Vector: [onset_hz, target_hz, duration_beats,
                 pitch_curve_type, intensity, raga_context]
        """
        return [
            onset_hz,
            target_hz,
            duration_beats,
            float(self.curve_type),
            intensity if intensity is not None else self.default_intensity,
            float(raga_context),
        ]

    def pitch_fn(
        self,
        onset_hz: float,
        target_hz: float,
        duration_s: float,
    ) -> Callable[[float], float]:
        """Return a pitch function f(t) → Hz for this gamaka.

        Args:
            onset_hz:   Starting frequency (Hz)
            target_hz:  Target frequency (Hz)
            duration_s: Total duration in seconds

        Returns:
            Callable f(t) where t ∈ [0, duration_s]
        """
        ct = self.curve_type
        A = (target_hz - onset_hz) * 0.02  # oscillation amplitude (2%)
        rate = self.default_rate

        if ct == PitchCurveType.FLAT:
            return lambda t: target_hz

        elif ct == PitchCurveType.LINEAR_UP:
            return lambda t: onset_hz + (target_hz - onset_hz) * (t / max(duration_s, 1e-6))

        elif ct == PitchCurveType.LINEAR_DOWN:
            return lambda t: onset_hz - (onset_hz - target_hz) * (t / max(duration_s, 1e-6))

        elif ct == PitchCurveType.OSCILLATE:
            amp = target_hz * 0.02
            return lambda t: target_hz + amp * math.sin(2 * math.pi * rate * t)

        elif ct == PitchCurveType.WIDE_OSCILLATE:
            amp = target_hz * 0.04
            slow_rate = 2.0
            return lambda t: target_hz + amp * math.sin(2 * math.pi * slow_rate * t)

        elif ct == PitchCurveType.GRACE_UP:
            # Brief touch above (5% higher) then settle at target
            eps = target_hz * 0.05
            transition = duration_s * 0.2
            def _grace_up(t: float) -> float:
                if t < transition:
                    return target_hz + eps * (1 - t / transition)
                return target_hz
            return _grace_up

        elif ct == PitchCurveType.GRACE_DOWN:
            eps = target_hz * 0.05
            transition = duration_s * 0.2
            def _grace_down(t: float) -> float:
                if t < transition:
                    return target_hz - eps * (1 - t / transition)
                return target_hz
            return _grace_down

        elif ct == PitchCurveType.ACCENT:
            # Slight pitch spike at attack
            spike = target_hz * 0.01
            attack = duration_s * 0.1
            def _accent(t: float) -> float:
                if t < attack:
                    return target_hz + spike * math.sin(math.pi * t / attack)
                return target_hz
            return _accent

        elif ct == PitchCurveType.FADE:
            return lambda t: target_hz  # volume handled by amplitude envelope

        else:
            # Complex — return flat as placeholder
            return lambda t: target_hz

    def __repr__(self) -> str:
        return f"Gamaka({self.token}, symbol={self.symbol!r}, {self.name})"


# ---------------------------------------------------------------------------
# All 15 Gamakas
# ---------------------------------------------------------------------------

GAMAKAS: dict[str, Gamaka] = {

    "GMK_KAMP": Gamaka(
        token="GMK_KAMP", symbol="~",
        name="Kampita", sanskrit="कम्पित",
        description="Vibrato-like oscillation between adjacent svaras.",
        curve_type=PitchCurveType.OSCILLATE,
        phonetic="kam-pi-ta",
        default_intensity=0.6, default_rate=6.0,
    ),

    "GMK_ANDO": Gamaka(
        token="GMK_ANDO", symbol="w",
        name="Andola", sanskrit="आन्दोल",
        description="Slow wide oscillation; pitch meanders without landing.",
        curve_type=PitchCurveType.WIDE_OSCILLATE,
        phonetic="aan-do-la",
        default_intensity=0.7, default_rate=2.0,
    ),

    "GMK_SPHU": Gamaka(
        token="GMK_SPHU", symbol="^",
        name="Sphurita", sanskrit="स्फुरित",
        description="Touch note above then land on target. Used in arohana.",
        curve_type=PitchCurveType.GRACE_UP,
        phonetic="sphoo-ri-ta",
        default_intensity=0.5,
    ),

    "GMK_PRAT": Gamaka(
        token="GMK_PRAT", symbol="v",
        name="Pratyaghata", sanskrit="प्रत्याघात",
        description="Touch note below then land on target. Used in avarohana.",
        curve_type=PitchCurveType.GRACE_DOWN,
        phonetic="prat-yaa-ghaa-ta",
        default_intensity=0.5,
    ),

    "GMK_NOKK": Gamaka(
        token="GMK_NOKK", symbol="*",
        name="Nokku", sanskrit="நொக்கு",
        description="Stress accent — forceful direct articulation.",
        curve_type=PitchCurveType.ACCENT,
        phonetic="nok-ku",
        default_intensity=0.9,
    ),

    "GMK_EJRU": Gamaka(
        token="GMK_EJRU", symbol="/",
        name="Etra Jaru", sanskrit="ஏற்ற ஜரு",
        description="Upward glide / portamento from lower svara to target.",
        curve_type=PitchCurveType.LINEAR_UP,
        phonetic="ay-tra ja-ru",
        default_intensity=0.6,
    ),

    "GMK_IJRU": Gamaka(
        token="GMK_IJRU", symbol="\\",
        name="Irakka Jaru", sanskrit="இறக்க ஜரு",
        description="Downward glide / portamento from higher svara to target.",
        curve_type=PitchCurveType.LINEAR_DOWN,
        phonetic="i-rak-ka ja-ru",
        default_intensity=0.6,
    ),

    "GMK_ORIK": Gamaka(
        token="GMK_ORIK", symbol="{or}",
        name="Orikkai", sanskrit="ஒரிக்கை",
        description="Subtle flick ornament; veena left-hand technique.",
        curve_type=PitchCurveType.COMPLEX,
        phonetic="o-rik-kai",
        default_intensity=0.4,
    ),

    "GMK_OTHU": Gamaka(
        token="GMK_OTHU", symbol="{ot}",
        name="Othukkal", sanskrit="ஒதுக்கல்",
        description="Pushing/pressing ornament; veena-specific.",
        curve_type=PitchCurveType.COMPLEX,
        phonetic="o-thuk-kal",
        default_intensity=0.5,
    ),

    "GMK_TRIB": Gamaka(
        token="GMK_TRIB", symbol="tr",
        name="Tribhinna", sanskrit="त्रिभिन्न",
        description="Three-string veena technique; three-pitch ornament.",
        curve_type=PitchCurveType.COMPLEX,
        phonetic="tri-bhin-na",
        default_intensity=0.6,
    ),

    "GMK_MUDR": Gamaka(
        token="GMK_MUDR", symbol="{mu}",
        name="Mudrita", sanskrit="मुद्रित",
        description="Muffled, nasal ornament (vocal only).",
        curve_type=PitchCurveType.COMPLEX,
        phonetic="mud-ri-ta",
        default_intensity=0.3,
    ),

    "GMK_NAMI": Gamaka(
        token="GMK_NAMI", symbol="{nm}",
        name="Namita", sanskrit="नमित",
        description="Gentle fading / decreasing volume ornament.",
        curve_type=PitchCurveType.FADE,
        phonetic="na-mi-ta",
        default_intensity=0.4,
    ),

    "GMK_MISR": Gamaka(
        token="GMK_MISR", symbol="gl",
        name="Misrita", sanskrit="मिश्रित",
        description="Mixed gamaka — blend of two types; generic glide.",
        curve_type=PitchCurveType.COMPLEX,
        phonetic="mis-ri-ta",
        default_intensity=0.5,
    ),

    "GMK_AHAT": Gamaka(
        token="GMK_AHAT", symbol="",
        name="Ahata", sanskrit="आहत",
        description="Direct attack, no embellishment. Default.",
        curve_type=PitchCurveType.FLAT,
        phonetic="aa-ha-ta",
        default_intensity=1.0,
    ),

    "GMK_ULLA": Gamaka(
        token="GMK_ULLA", symbol="vib",
        name="Ullasita / Vibrato", sanskrit="उल्लसित",
        description="Rapid mordent-like ornament; sustained vibrato variant.",
        curve_type=PitchCurveType.OSCILLATE,
        phonetic="ul-la-si-ta",
        default_intensity=0.7, default_rate=8.0,
    ),
}

# ---------------------------------------------------------------------------
# Symbol → Token lookup
# ---------------------------------------------------------------------------

GAMAKA_SYMBOLS: dict[str, str] = {
    gm.symbol: token
    for token, gm in GAMAKAS.items()
    if gm.symbol  # skip empty symbol (Ahata)
}

# Add verbose aliases
GAMAKA_SYMBOLS.update({
    "~~":  "GMK_KAMP",   # legacy double-tilde
    "nd":  "GMK_ANDO",   # andola alias
    "sp":  "GMK_SPHU",   # sphurita alias
    "{tr}":"GMK_TRIB",
    "{gl}":"GMK_MISR",
})


def parse_gamaka_symbol(sym: str) -> Gamaka | None:
    """Resolve a notation symbol to its Gamaka definition.

    Args:
        sym: e.g. "~", "/", "\\\\", "^", "w", "tr", "vib"

    Returns:
        Gamaka instance, or None if not found (= Ahata)
    """
    token = GAMAKA_SYMBOLS.get(sym)
    if token:
        return GAMAKAS[token]
    return GAMAKAS["GMK_AHAT"]  # default — direct, no ornament


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n─── 15 Gamakas ───────────────────────────────────────────")
    for token, gm in GAMAKAS.items():
        sym = f"'{gm.symbol}'" if gm.symbol else "(none)"
        print(f"  {token:12s}  sym={sym:8s}  {gm.name:20s}  curve={gm.curve_type.name}")

    # Feature vector example
    kamp = GAMAKAS["GMK_KAMP"]
    vec = kamp.feature_vector(onset_hz=288.0, target_hz=320.0, duration_beats=1.0)
    print(f"\nKampita feature vector: {vec}")

    # Pitch function example
    fn = kamp.pitch_fn(onset_hz=288.0, target_hz=288.0, duration_s=0.5)
    samples = [fn(t * 0.1) for t in range(6)]
    print(f"Kampita pitch samples (0–0.5s): {[f'{h:.1f}' for h in samples]} Hz")
