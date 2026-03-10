# 🎵 RagaNotate

> **Full-Stack Carnatic Music Notation Engine**
> A human-readable, AI-compatible notation system for Carnatic classical music.

[![Version](https://img.shields.io/badge/version-0.1.0-gold)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-Phase%201%20Complete-green)](#roadmap)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](packages/python/)
[![TypeScript](https://img.shields.io/badge/typescript-5.x-blue)](packages/js/)
[![Author](https://img.shields.io/badge/author-jags111-purple)](https://github.com/jags111)

---

## Overview

**RagaNotate** is a full-stack Carnatic music notation system that bridges human musicians and AI/ML systems. It provides:

- A clean **ASCII + Unicode notation format** for human-readable Carnatic swaras, gamakas, and talas
- A **TypeScript/JS library** for parsing notation strings into SVG visual output
- A **Python package** (`raganotate`) for parsing, MIDI export, and AI tokenization
- A **Web UI** with a live notation editor and gamaka pitch contour visualizer
- An **AI-ready dataset** of annotated Carnatic compositions for ML training

**Inspired by:** [srikumarks/carnot](https://github.com/srikumarks/carnot) · [ragasangrah.com](https://ragasangrah.com/gamakas) · iSargam (Springer 2016) · *Sangita Sampradaya Pradarshini*

---

## Quick Start — Notation Format

```
# Octaves
MANDRA:  .s  .r  .g  .m  .p  .d  .n      (lower octave)
MADHYA:   S   R   G   M   P   D   N       (middle octave)
TARA:    S'  R'  G'  M'  P'  D'  N'      (upper octave)

# Duration
S    = 1 akshara (full beat)
S;   = 2 aksharas (double duration)
S:   = 0.5 aksharas (half)
S::  = 0.25 aksharas (quarter)

# Beat Markers
|   = Beat separator       ,  = Half-beat gap
||  = Section end          -  = Rest / pause
_   = Invisible grace gap

# Gamakas
~~   = Kampita (vibrato)   ^   = Etra Jaru (slide up)
v    = Irakka Jaru (slide down)
*    = Nokku (stress)      (^) = Sphurita   (v) = Pratyaghata

# Example — Adi Tala, Madhya Sthayi
| S R~~ G M | P^D N S' | N v D P | M G R S |
```

---

## Repository Structure

```
RagaNotate/
├── README.md                   ← You are here
├── CHANGELOG.md                ← Version history
├── SPEC.md                     ← Full notation specification
├── todo.md                     ← Project roadmap & master TODO
├── LICENSE
├── .gitignore
├── CONTRIBUTING.md
│
├── spec/
│   ├── PHONETICS.md            ← 16 Swarasthana phonetic encoding
│   ├── GAMAKAS.md              ← 15 Gamakas reference + AI vectors
│   └── TALAS.md                ← Suladi Sapta + Chapu + 108-tala system
│
├── packages/
│   ├── js/                     ← TypeScript/JS library
│   │   ├── src/
│   │   │   ├── lexer.ts        ← Tokenizer
│   │   │   ├── parser.ts       ← AST builder
│   │   │   ├── renderer.ts     ← SVG output
│   │   │   ├── gamaka.ts       ← Pitch contour engine
│   │   │   └── tala.ts         ← Beat pattern generator
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── python/                 ← Python package
│       ├── raganotate/
│       │   ├── __init__.py
│       │   ├── swara.py        ← Swara + Swarasthana classes
│       │   ├── gamaka.py       ← Gamaka types + AI feature vectors
│       │   ├── tala.py         ← Tala + Anga system
│       │   ├── parser.py       ← ASCII notation → Python objects
│       │   ├── renderer.py     ← MIDI / LilyPond / MusicXML export
│       │   ├── ai_encoder.py   ← Notation → AI tokens
│       │   └── dataset.py      ← Dataset utilities for ML
│       ├── tests/
│       └── setup.py
│
├── web/                        ← Web UI
│   ├── index.html
│   ├── editor.html
│   └── assets/
│
├── examples/                   ← Sample compositions
│   ├── ganarajena.txt
│   ├── sri_ganesha.txt
│   └── vathapi.txt
│
└── dataset/                    ← AI training data
    ├── annotated/
    └── gamaka_labels.json
```

---

## Roadmap

| Version | Phase | Status |
|---------|-------|--------|
| **v0.1.0** | Phase 1 — Core Specification | ✅ Complete |
| v0.2.0 | Phase 2 — TypeScript Library | 🔲 Next |
| v0.3.0 | Phase 3 — Python `raganotate` Package | 🔲 Planned |
| v0.4.0 | Phase 4 — Web UI Editor | 🔲 Planned |
| v0.5.0 | Phase 5 — GitHub CI/CD + Examples | 🔲 Planned |
| v1.0.0 | Phase 6 — Dataset + AI Release | 🔲 Planned |

See [CHANGELOG.md](CHANGELOG.md) for full version history and [todo.md](todo.md) for detailed task breakdown.

---

## The 16 Swarasthanas

| # | Symbol | Phonetic | AI Token | Ratio | Hz @ Sa=240 |
|---|--------|----------|----------|-------|-------------|
| 1 | S  | Sa  | SA_0  | 1/1    | 240.00 |
| 2 | r  | Ra  | RI_1  | 256/243 | 252.84 |
| 3 | R  | Ri  | RI_2  | 9/8    | 270.00 |
| 4 | g  | Ga  | GA_1  | 32/27  | 284.44 |
| 5 | G  | Gi  | GA_2  | 6/5    | 288.00 |
| 6 | G+ | Gu  | GA_3  | 5/4    | 300.00 |
| 7 | m  | Ma  | MA_1  | 4/3    | 320.00 |
| 8 | M  | Mi  | MA_2  | 45/32  | 337.50 |
| 9 | P  | Pa  | PA_0  | 3/2    | 360.00 |
| 10 | d | Da  | DA_1  | 128/81 | 379.26 |
| 11 | D | Di  | DA_2  | 5/3    | 400.00 |
| 12 | n | Na  | NI_1  | 16/9   | 426.67 |
| 13 | N | Ni  | NI_2  | 9/5    | 432.00 |
| 14 | N+ | Nu | NI_3  | 15/8   | 450.00 |
| 15 | S' | Sa' | SA_0_HI | 2/1  | 480.00 |
| 16 | .s | .sa | SA_0_LO | 1/2  | 120.00 |

---

## Python Usage (Coming in v0.3.0)

```python
from raganotate import swara_hz, print_scale

# Get frequency of any swara
hz = swara_hz("G", octave="tara", sa_hz=240.0)
print(f"Antara Gandharam (tara): {hz} Hz")

# Print full scale for Sa = 261.63 Hz (C4)
print_scale(261.63)
```

---

## References

- [srikumarks/carnot](https://github.com/srikumarks/carnot) — JavaScript SVG rendering engine for Carnatic notation
- [ragasangrah.com/gamakas](https://ragasangrah.com/gamakas) — Gamaka reference
- [iSargam (Springer 2016)](https://link.springer.com/article/10.1186/s13636-016-0083-z) — Unicode-based Indian notation encoding
- [karnatik.com/symbols](https://www.karnatik.com/symbols.shtml) — Standard notation symbols
- [saayujya.com — Gamaka Notation](https://saayujya.com/index.php/2019/12/03/gamaka-notation/)
- [Upbeat Labs — Tala Primer](https://www.upbeatlabs.com/2017/01/17/a-primer-for-carnatic-talas/)
- *Sangita Sampradaya Pradarshini* — Subbarama Dikshitar
- *Natya Shastra* — Bharata Muni

---

## Author

**Jags** · [@jags111](https://github.com/jags111) · [info@revsmartasia.com](mailto:info@revsmartasia.com)

---

## License

MIT © 2026 Jags (jags111). See [LICENSE](LICENSE).
