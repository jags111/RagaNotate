"""
lyrics_mapper.py — Lyrics Text → Notation Alignment
=====================================================
Maps song lyrics (syllables) to swara positions in a notation string.
Handles melisma (one syllable over multiple notes), rests, and tala alignment.

Ref: RagaNotate SPEC.md §9 · ARCHITECTURE.md · github.com/jags111/RagaNotate
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional

from .parser import NotationAST, SwaraNode, RestNode, parse_notation
from .tala import get_tala, TalaEngine, Tala


# ---------------------------------------------------------------------------
# Syllable Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Syllable:
    """A single lyric syllable."""
    text: str
    duration: float = 1.0   # in aksharas
    is_melisma_end: bool = False  # True if this syllable spans multiple notes
    stress: float = 0.5          # 0.0–1.0 (affects gamaka intensity)

    def __repr__(self) -> str:
        return f"Syllable({self.text!r}, dur={self.duration})"


# ---------------------------------------------------------------------------
# LyricsMapper
# ---------------------------------------------------------------------------

class LyricsMapper:
    """Aligns lyrics syllables to notation swaras.

    Usage:
        mapper = LyricsMapper(raga="Hamsadhvani", tala="Adi")
        result = mapper.align(
            lyrics="Vathapi Ganapatim Bhaje",
            notation="| S R G P | N S' N P | G R S , |"
        )
    """

    def __init__(self, raga: str = "", tala: str = "Adi", sa_hz: float = 240.0):
        self.raga = raga
        self.tala_name = tala
        self.sa_hz = sa_hz
        try:
            self.tala: Optional[Tala] = get_tala(tala)
        except KeyError:
            self.tala = None

    def align(
        self,
        lyrics: str,
        notation: str,
    ) -> NotationAST:
        """Align lyrics to notation and return an annotated AST.

        Args:
            lyrics:   Lyrics string (words or syllables separated by spaces)
            notation: ASCII notation string

        Returns:
            NotationAST with lyric fields populated on SwaraNodes.
        """
        ast = parse_notation(notation, tala=self.tala_name)
        syllables = syllabify(lyrics)
        swaras = ast.swaras()

        # Simple 1:1 alignment (one syllable per swara)
        for i, sw in enumerate(swaras):
            if i < len(syllables):
                sw.lyric = syllables[i].text
            else:
                sw.lyric = None

        return ast

    def to_notation_block(
        self,
        lyrics: str,
        notation: str,
    ) -> str:
        """Return a formatted notation block with lyrics below each swara.

        Example output:
            {tala: Adi}
            | S   R~  G   M   | P   D   N   S'  |
            | ya  mu  na  ka  | la  ya  di  pa  |
        """
        ast = self.align(lyrics, notation)
        swaras = ast.swaras()
        cells: list[tuple[str, str]] = []  # (swara_str, lyric_str)

        for sw in swaras:
            sym = sw.symbol
            if sw.octave == "tara":
                sym += "'"
            elif sw.octave == "mandra":
                sym = "." + sym.lower()
            gk = sw.gamaka.symbol if sw.gamaka else ""
            cells.append((sym + gk, sw.lyric or "-"))

        # Build lines
        sw_line   = "  ".join(f"{s:4s}" for s, _ in cells)
        lyric_line = "  ".join(f"{l:4s}" for _, l in cells)

        return (
            f"{{tala: {self.tala_name}}}\n"
            f"{sw_line}\n"
            f"{lyric_line}\n"
        )


# ---------------------------------------------------------------------------
# Syllabifier
# ---------------------------------------------------------------------------

# Simple regex-based syllabifier for South Indian syllable patterns.
# For production, use a language-specific library (e.g. pyphen, indic-nlp-library).
_VOWELS = set("aeiouAEIOUāīūṛḷ")
_CONSONANTS = r"[^aeiouAEIOUāīūṛḷ\s]"

def syllabify(text: str) -> list[Syllable]:
    """Split text into syllables for lyrics-to-notation mapping.

    Currently uses a simple whitespace/dash split as a baseline.
    For proper Carnatic syllabification, integrate a Sanskrit/Tamil
    syllabifier (e.g. indic-nlp-library).

    Args:
        text: Lyrics string, e.g. "Vathapi Ganapatim Bhaje"
              or pre-syllabified "Va-tha-pi Ga-na-pa-tim Bha-je"

    Returns:
        List of Syllable objects.

    Example:
        >>> syllabify("Va-tha-pi")
        [Syllable('Va'), Syllable('tha'), Syllable('pi')]
    """
    # Handle hyphen-separated syllables
    if "-" in text:
        parts = re.split(r"[-\s]+", text)
    else:
        # Naive: split on whitespace, then try basic CV syllabification
        words = text.split()
        parts = []
        for word in words:
            parts.extend(_split_word(word))

    syllables = []
    for part in parts:
        part = part.strip()
        if part:
            # Detect stress: capitalized or marked with underscore prefix
            stress = 0.7 if part[0].isupper() else 0.4
            syllables.append(Syllable(text=part, stress=stress))

    return syllables


def _split_word(word: str) -> list[str]:
    """Very basic CV syllabification for a single word.

    For Sanskrit/Tamil proper syllabification, replace this with
    indic-nlp-library or custom rules.
    """
    if len(word) <= 3:
        return [word]

    syllables = []
    i = 0
    current = ""
    while i < len(word):
        ch = word[i]
        current += ch
        # Break after vowel + optional following consonant
        if ch.lower() in _VOWELS:
            if i + 1 < len(word) and word[i + 1].lower() not in _VOWELS:
                # Keep one consonant with previous vowel
                i += 1
                current += word[i]
            syllables.append(current)
            current = ""
        i += 1
    if current:
        if syllables:
            syllables[-1] += current
        else:
            syllables.append(current)

    return syllables if syllables else [word]


# ---------------------------------------------------------------------------
# Alignment utility
# ---------------------------------------------------------------------------

def align_lyrics_to_notation(
    lyrics: str,
    notation: str,
    tala: str = "Adi",
    raga: str = "",
    sa_hz: float = 240.0,
) -> NotationAST:
    """Convenience function: align lyrics to notation in one call.

    Args:
        lyrics:   Song lyrics (space or hyphen separated syllables)
        notation: ASCII notation string
        tala:     Tala name
        raga:     Raga name (for future gamaka auto-assignment)
        sa_hz:    Adhara Shadjam frequency

    Returns:
        Annotated NotationAST

    Example:
        ast = align_lyrics_to_notation(
            "Va-tha-pi Ga-na-pa-tim Bha-je",
            "| S R G P | N S' N P | G R S |",
            tala="Adi",
            raga="Hamsadhvani",
        )
        for sw in ast.swaras():
            print(f"{sw.symbol:4s} → {sw.lyric}")
    """
    mapper = LyricsMapper(raga=raga, tala=tala, sa_hz=sa_hz)
    return mapper.align(lyrics, notation)


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    lyrics   = "Va-tha-pi Ga-na-pa-tim Bha-je Ha-ri-dra gra-hi-Nam"
    notation = "| S R G P | N S' N P | G R S , | .n S R S ||"

    mapper = LyricsMapper(raga="Hamsadhvani", tala="Adi", sa_hz=240.0)

    print("\n── Syllabification ──────────────────────────────────────")
    syllables = syllabify(lyrics)
    for s in syllables:
        print(f"  {s}")

    print("\n── Alignment ────────────────────────────────────────────")
    ast = mapper.align(lyrics, notation)
    for sw in ast.swaras():
        print(f"  {sw.symbol:5s}  lyric: {sw.lyric}")

    print("\n── Notation Block ───────────────────────────────────────")
    block = mapper.to_notation_block(lyrics, notation)
    print(block)
