"""
RagaNotate — Full-Stack Carnatic Music Notation Engine
=======================================================
github.com/jags111/RagaNotate

Converts lyrics and ASCII notation into:
  - Visual SVG notation
  - MIDI files with gamaka pitch bends
  - Audio waveforms (scipy/numpy synthesis)
  - AI-ready token sequences

Quick Start
-----------
    from raganotate import swara_hz, print_scale, parse_notation

    # Frequencies
    print_scale(sa_hz=240.0)
    hz = swara_hz("G3", octave="madhya", sa_hz=240.0)

    # Parse notation
    ast = parse_notation("| S R~ G M | P/D N S' |", tala="Adi")

Version: 0.1.4
Author:  Jags (jags111) · github.com/jags111
"""

from .swara import (
    SWARASTHANAS,
    OCTAVE_MULTIPLIER,
    swara_hz,
    print_scale,
)
from .gamaka import (
    GAMAKAS,
    GAMAKA_SYMBOLS,
    parse_gamaka_symbol,
)
from .tala import (
    TALAS,
    CHAPU_TALAS,
    Tala,
    TalaEngine,
    get_tala,
)
from .parser import (
    parse_notation,
    NotationAST,
    SwaraNode,
    TalaNode,
)
from .lyrics_mapper import (
    LyricsMapper,
    syllabify,
    align_lyrics_to_notation,
)

__version__ = "0.1.4"
__author__ = "Jags (jags111)"
__repo__ = "https://github.com/jags111/RagaNotate"

__all__ = [
    # swara
    "SWARASTHANAS", "OCTAVE_MULTIPLIER", "swara_hz", "print_scale",
    # gamaka
    "GAMAKAS", "GAMAKA_SYMBOLS", "parse_gamaka_symbol",
    # tala
    "TALAS", "CHAPU_TALAS", "Tala", "TalaEngine", "get_tala",
    # parser
    "parse_notation", "NotationAST", "SwaraNode", "TalaNode",
    # lyrics
    "LyricsMapper", "syllabify", "align_lyrics_to_notation",
]
