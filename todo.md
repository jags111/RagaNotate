# 🎵 Carnatic Notation System — Master TODO & Specification
> **Project:** Full-Stack Carnatic Music Notation Engine
> **Author:** Jags (jags111) · [github.com/jags111](https://github.com/jags111)
> **Repository:** [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)
> **Date:** 2026-03-10
> **Version:** v0.1.0 — Phase 1 Complete (see [CHANGELOG.md](CHANGELOG.md))
> **Status:** In Progress — Phase 2 (TypeScript Library) next
> **Inspired by:** [srikumarks/carnot](https://github.com/srikumarks/carnot), [ragasangrah.com](https://ragasangrah.com/gamakas), iSargam (Springer), Sangita Sampradaya Pradarshini

---

## 📋 TABLE OF CONTENTS
1. [Project Overview](#1-project-overview)
2. [Notation Standard — Swaras & Octaves](#2-notation-standard--swaras--octaves)
3. [16 Swarasthanas — Phonetic Encoding](#3-16-swarasthanas--phonetic-encoding)
4. [15 Gamakas — Full AI Encoding](#4-15-gamakas--full-ai-encoding)
5. [Tala System — Anga Notation](#5-tala-system--anga-notation)
6. [Full Deliverables Roadmap](#6-full-deliverables-roadmap)
7. [Repository Structure](#7-repository-structure)
8. [Implementation Phases](#8-implementation-phases)
9. [References](#9-references)

---

## 1. PROJECT OVERVIEW

### Vision
A **full-stack Carnatic music notation system** that allows:
- Human musicians to read/write Carnatic notation in a clean ASCII+Unicode format
- AI/ML models to parse, classify, and synthesize Carnatic phrases
- Web-based rendering (SVG) of notation — prescriptive AND descriptive
- Gamaka encoding for training TTS/audio synthesis models
- Tala beat-map generation for rhythm accompaniment systems

### Deliverables
| # | Deliverable | Format | Priority |
|---|-------------|--------|----------|
| 1 | **Notation Specification** | Markdown (`SPEC.md`) | ✅ High |
| 2 | **TypeScript/JS rendering library** | `.ts` / `.js` | ✅ High |
| 3 | **Python parser & notation tools** | `pip` package | ✅ High |
| 4 | **Web UI** — live notation editor | HTML + JS | ✅ High |
| 5 | **Workflow chart** | HTML interactive | ✅ High |
| 6 | **Dataset** — annotated notation samples | JSON/CSV | 🔶 Medium |
| 7 | **GitHub repository** setup | github.com/jags111 | 🔶 Medium |

---

## 2. NOTATION STANDARD — SWARAS & OCTAVES

### Octave Markers (Your Standard — ADOPTED)

```
TARA STHAYI  (Upper Octave):  S'  R'  G'  M'  P'  D'  N'
MADHYA STHAYI (Middle Octave): S   R   G   M   P   D   N
MANDRA STHAYI (Lower Octave): .s  .r  .g  .m  .p  .d  .n
```

### Beat Marker
```
|   = Beat / Avartanam separator
||  = End of composition section
,   = Half-beat gap (visible)
_   = Grace note gap (invisible timing)
-   = Pause / rest
```

### Duration Markers
```
S    = 1 akshara (full beat)
S;   = 2 aksharas (double duration)
S:   = 0.5 aksharas (half duration)
S::  = 0.25 aksharas (quarter duration)
```

### Full Notation Example (Adi Tala, Madhya Sthayi)
```
| S R G M | P D N S' | N D P M | G R S , |
```

---

## 3. 16 SWARASTHANAS — PHONETIC ENCODING & FREQUENCY RATIOS

### Design Rules (AI-Compatible)
- **Suffix 'a'** → Lower / Suddha variant
- **Suffix 'i'** → Middle / Chatusruti variant
- **Suffix 'u'** → Higher / Shatsruti variant
- Combines with octave markers: `.sa`, `Sa`, `Sa'`

### Frequency System — Adhara Shadjam (Just Intonation)

> **Key Rule:** Sa is **relative**, not absolute. All frequencies are ratios of Sa.
> Once the performer fixes their Adhara Shadjam (Sa), all 16 swarasthanas
> are mathematically determined by the ratios below.
>
> Common Sa values: **240 Hz** (traditional), **256 Hz** (scientific pitch),
> **261.63 Hz** (C4, Western concert pitch), **220 Hz** (lower male voice).

#### 7-Swara Frequency Table (Jags' Standard, Sa = 240 Hz)

| Swara | Ratio | Hz (Sa=240) | Hz (Sa=256) | Hz (Sa=261.63) | Notes |
|-------|-------|------------|------------|----------------|-------|
| **Sa** | 1/1 | 240.00 | 256.00 | 261.63 | Tonic (Achala) |
| **Ri** | 9/8 | 270.00 | 288.00 | 294.33 | Chatusruti Ri |
| **Ga** | 6/5 | 288.00 | 307.20 | 313.96 | Sadharana Ga |
| **Ga** | 5/4 | 300.00 | 320.00 | 327.04 | Antara Ga (alt.) |
| **Ma** | 4/3 | 320.00 | 341.33 | 348.83 | Suddha Ma |
| **Ma** | 17/12 | 340.00 | 362.67 | 370.64 | Prati Ma (alt.) |
| **Pa** | 3/2 | 360.00 | 384.00 | 392.44 | Panchama (Achala) |
| **Dha** | 27/16 | 405.00 | 432.00 | 441.49 | Chatusruti Dha |
| **Dha** | 5/3 | 400.00 | 426.67 | 436.05 | Suddha Dha (alt.) |
| **Ni** | 9/5 | 432.00 | 460.80 | 470.93 | Kaisika Ni ← *432 Hz* |
| **Ni** | 15/8 | 450.00 | 480.00 | 490.55 | Kakali Ni |
| **Sa'** | 2/1 | 480.00 | 512.00 | 523.25 | Upper octave |

> ⚠️ **Note on 432 Hz:** With Sa = 240 Hz, the value 432 Hz corresponds to
> **Kaisika Nishadam** (ratio 9/5), *not* Kakali Nishadam (ratio 15/8 = 450 Hz).
> Both are valid — the raga determines which Ni is used.

---

### Complete 16-Swarasthana Table (Just Intonation)

| # | Swara Name | Short | Phonetic | AI Token | Ratio | Hz@240 | Hz@261.63 | Type |
|---|-----------|-------|----------|----------|-------|--------|-----------|------|
| 1 | Shadjam | S | Sa | SA_0 | 1/1 | 240.00 | 261.63 | Achala |
| 2 | Suddha Rishabham | r | Ra | RI_1 | 256/243 | 252.84 | 275.62 | Chala |
| 3 | Chatusruti Rishabham | R | Ri | RI_2 | 9/8 | 270.00 | 294.33 | Chala |
| 4 | Shatsruti Ri / Suddha Ga | g | Ga | GA_1 | 32/27 | 284.44 | 309.87 | Chala |
| 5 | Sadharana Gandharam | G | Gi | GA_2 | 6/5 | 288.00 | 313.96 | Chala |
| 6 | Antara Gandharam | G+ | Gu | GA_3 | 5/4 | 300.00 | 327.04 | Chala |
| 7 | Suddha Madhyamam | m | Ma | MA_1 | 4/3 | 320.00 | 348.83 | Chala |
| 8 | Prati Madhyamam | M | Mi | MA_2 | 45/32 | 337.50 | 367.92 | Chala |
| 9 | Panchamam | P | Pa | PA_0 | 3/2 | 360.00 | 392.44 | Achala |
| 10 | Suddha Dhaivatam | d | Da | DA_1 | 128/81 | 379.26 | 413.43 | Chala |
| 11 | Chatusruti Dhaivatam | D | Di | DA_2 | 5/3 | 400.00 | 436.05 | Chala |
| 12 | Shatsruti Dha / Suddha Ni | n | Na | NI_1 | 16/9 | 426.67 | 465.11 | Chala |
| 13 | Kaisika Nishadam | N | Ni | NI_2 | 9/5 | 432.00 | 470.93 | Chala |
| 14 | Kakali Nishadam | N+ | Nu | NI_3 | 15/8 | 450.00 | 490.55 | Chala |
| 15 | Upper Shadjam | S' | Sa' | SA_0_HI | 2/1 | 480.00 | 523.25 | Achala |
| 16 | Lower Shadjam | .s | .sa | SA_0_LO | 1/2 | 120.00 | 130.81 | Achala |

> **Shared pitches:** R3 (Shatsruti Ri) = G1 (Suddha Ga) · D3 (Shatsruti Dha) = N1 (Suddha Ni)
> — same frequency, different names depending on raga context.

---

### Python Frequency Calculator

```python
# RagaNotate — Swara Frequency Engine
# github.com/jags111/RagaNotate

from fractions import Fraction

# Adhara Shadjam — set your tonic here
SA_HZ = 240.0   # Change to 256, 261.63, 220, etc.

# 16 Swarasthanas — Just Intonation Ratios
SWARASTHANAS = {
    "S":  {"name": "Shadjam",              "phonetic": "Sa",  "token": "SA_0",  "ratio": Fraction(1, 1),    "type": "achala"},
    "r":  {"name": "Suddha Rishabham",     "phonetic": "Ra",  "token": "RI_1",  "ratio": Fraction(256,243), "type": "chala"},
    "R":  {"name": "Chatusruti Rishabham", "phonetic": "Ri",  "token": "RI_2",  "ratio": Fraction(9, 8),    "type": "chala"},
    "g":  {"name": "Suddha Gandharam",     "phonetic": "Ga",  "token": "GA_1",  "ratio": Fraction(32, 27),  "type": "chala"},
    "G":  {"name": "Sadharana Gandharam",  "phonetic": "Gi",  "token": "GA_2",  "ratio": Fraction(6, 5),    "type": "chala"},
    "G+": {"name": "Antara Gandharam",     "phonetic": "Gu",  "token": "GA_3",  "ratio": Fraction(5, 4),    "type": "chala"},
    "m":  {"name": "Suddha Madhyamam",     "phonetic": "Ma",  "token": "MA_1",  "ratio": Fraction(4, 3),    "type": "chala"},
    "M":  {"name": "Prati Madhyamam",      "phonetic": "Mi",  "token": "MA_2",  "ratio": Fraction(45, 32),  "type": "chala"},
    "P":  {"name": "Panchamam",            "phonetic": "Pa",  "token": "PA_0",  "ratio": Fraction(3, 2),    "type": "achala"},
    "d":  {"name": "Suddha Dhaivatam",     "phonetic": "Da",  "token": "DA_1",  "ratio": Fraction(128, 81), "type": "chala"},
    "D":  {"name": "Chatusruti Dhaivatam", "phonetic": "Di",  "token": "DA_2",  "ratio": Fraction(5, 3),    "type": "chala"},
    "n":  {"name": "Suddha Nishadam",      "phonetic": "Na",  "token": "NI_1",  "ratio": Fraction(16, 9),   "type": "chala"},
    "N":  {"name": "Kaisika Nishadam",     "phonetic": "Ni",  "token": "NI_2",  "ratio": Fraction(9, 5),    "type": "chala"},
    "N+": {"name": "Kakali Nishadam",      "phonetic": "Nu",  "token": "NI_3",  "ratio": Fraction(15, 8),   "type": "chala"},
}

# Octave multipliers
OCTAVE = {"mandra": 0.5, "madhya": 1.0, "tara": 2.0}

def swara_hz(symbol: str, octave: str = "madhya", sa_hz: float = SA_HZ) -> float:
    """Calculate frequency of a swara in Hz.

    Args:
        symbol: Swara symbol (S, R, G, m, M, P, D, N, etc.)
        octave: 'mandra', 'madhya', or 'tara'
        sa_hz: Adhara Shadjam frequency in Hz
    Returns:
        Frequency in Hz (just intonation)
    """
    s = SWARASTHANAS[symbol]
    return float(s["ratio"]) * sa_hz * OCTAVE[octave]

def print_scale(sa_hz: float = SA_HZ):
    """Print all 16 swarasthanas with frequencies for a given Sa."""
    print(f"\n{'─'*60}")
    print(f"  RagaNotate — Swara Frequencies  (Sa = {sa_hz} Hz)")
    print(f"{'─'*60}")
    for sym, s in SWARASTHANAS.items():
        hz = float(s["ratio"]) * sa_hz
        print(f"  {sym:4s} {s['phonetic']:4s}  {str(s['ratio']):8s}  {hz:8.2f} Hz  {s['name']}")
    print(f"  S'   Sa'  2/1      {sa_hz*2:.2f} Hz  Upper Shadjam")
    print(f"{'─'*60}\n")

# Example usage
if __name__ == "__main__":
    print_scale(240.0)   # Traditional
    print_scale(261.63)  # C4 concert pitch
```

### AI Phonetic Encoding — Vowel Rules
```
Suffix 'a'  →  Suddha (lower) variant:      Ra (Suddha Ri),  Da (Suddha Dha)
Suffix 'i'  →  Chatusruti (middle) variant: Ri (Chatusruti Ri), Di (Chatusruti Dha)
Suffix 'u'  →  Kakali/Shatsruti variant:    Nu (Kakali Ni)

Full AI token: {octave}_{swara}_{variant}
  Octave prefix:  LO_ (mandra) · MD_ (madhya) · HI_ (tara)
  Example: HI_RI_2 = Chatusruti Rishabham in Tara Sthayi
```

---

## 4. 15 GAMAKAS — FULL AI ENCODING

### Reference Sources
- *Sangita Sampradaya Pradarshini* (Subbarama Dikshitar)
- *Natya Shastra* (Bharata Muni — original 15 gamaka classification)
- iSargam Unicode encoding (Springer, 2016)
- Computer Synthesis research: gamakam.tripod.com

### Gamaka Notation Symbols
| Symbol | Meaning |
|--------|---------|
| `~` | Generic gamaka / ornament (tilde over swara) |
| `^` | Upward slide (Jaru upward) |
| `v` | Downward slide (Jaru downward) |
| `~~` | Kampita (vibrato-like oscillation) |
| `(` `)` | Sphurita / grace-note grouping |
| `<` `>` | Pitch bend down / up |
| `*` | Nokku (stress accent / snap) |
| `=` | Held note (no gamaka) |
| `{..}` | Gamaka block — full descriptive |

### Complete 15 Gamakas Table

| # | Name | Sanskrit | Description | AI Token | Notation | Phonetic |
|---|------|----------|-------------|----------|----------|----------|
| 1 | **Kampita** | कम्पित | Oscillation/vibrato between adjacent svaras. Like Western vibrato. On veena: shake the string. | `GMK_KAMP` | `~~` | "kam-pi-ta" |
| 2 | **Andola** | आन्दोल | Slow, wide oscillation. Pitch meanders between neighbours without landing on the svara itself. | `GMK_ANDO` | `~^~` | "aan-do-la" |
| 3 | **Sphurita** | स्फुरित | A grace note: touch the note above then land on target. Used in arohana. | `GMK_SPHU` | `(^)` | "sphoo-ri-ta" |
| 4 | **Pratyaghata** | प्रत्याघात | Reverse grace: touch the note below then land on target. Used in avarohana. | `GMK_PRAT` | `(v)` | "prat-yaa-ghaa-ta" |
| 5 | **Nokku** | நொக்கு | Stress accent — a sudden forceful articulation of a note. | `GMK_NOKK` | `*` | "nok-ku" |
| 6 | **Etra Jaru** | ஏற்ற ஜரு | Upward glide / portamento from lower svara to target. | `GMK_EJRU` | `^` | "ay-tra ja-ru" |
| 7 | **Irakka Jaru** | இறக்க ஜரு | Downward glide / portamento from higher svara to target. | `GMK_IJRU` | `v` | "i-rak-ka ja-ru" |
| 8 | **Orikkai** | ஒரிக்கை | A subtle flick or ornament used mainly on veena (left-hand technique). | `GMK_ORIK` | `{or}` | "o-rik-kai" |
| 9 | **Othukkal** | ஒதுக்கல் | A pushing / pressing ornament — veena-specific. Note pushed and held. | `GMK_OTHU` | `{ot}` | "o-thuk-kal" |
| 10 | **Tribhinna** | त्रिभिन्न | Three-string technique on veena — flattened finger on three strings simultaneously. | `GMK_TRIB` | `{tr}` | "tri-bhin-na" |
| 11 | **Mudrita** | मुद्रित | Ornament with mouth closed (vocal only). A muffled, nasal ornament. | `GMK_MUDR` | `{mu}` | "mud-ri-ta" |
| 12 | **Namita** | नमित | Decreasing volume ornament — gentle fading of a note. | `GMK_NAMI` | `{nm}` | "na-mi-ta" |
| 13 | **Misrita** | मिश्रित | Mixed/combined gamaka — a blend of two gamaka types. | `GMK_MISR` | `{mx}` | "mis-ri-ta" |
| 14 | **Ahata** | आहत | Struck note — the svara is played with full, direct attack. No embellishment. | `GMK_AHAT` | `=` | "aa-ha-ta" |
| 15 | **Ullasita** | उल्लसित | Sparkling, joyful ornament — rapid mordent-like movement. | `GMK_ULLA` | `{ul}` | "ul-la-si-ta" |

### AI Gamaka Vector Encoding (for ML)
Each gamaka encoded as a 6-dimensional feature vector:
```
[onset_pitch, target_pitch, duration_beats, pitch_curve_type, intensity, raga_context]

pitch_curve_type:
  0 = flat (ahata)
  1 = linear_up (etra jaru)
  2 = linear_down (irakka jaru)
  3 = oscillate (kampita)
  4 = wide_oscillate (andola)
  5 = grace_up (sphurita)
  6 = grace_down (pratyaghata)
  7 = accent (nokku)
  8 = fade (namita)
  9 = complex (misrita / ullasita)
```

---

## 5. TALA SYSTEM — ANGA NOTATION

### The Three Core Angas (Suladi Sapta Tala System)

| Anga | Symbol | Duration | Hand Action |
|------|--------|----------|-------------|
| **Anudhrutam** | `U` | 1 akshara | Downward palm-down clap |
| **Dhrutam** | `O` | 2 aksharas | Palm-down + palm-up clap |
| **Laghu** | `l` or `\|` | Variable (3/4/5/7/9) | Clap + finger count |

### Laghu Jaati (Rhythmic Subdivisions)

| Jaati Name | Aksharas | Symbol | Mnemonic |
|------------|----------|--------|----------|
| Tisra | 3 | `l3` | Tha Ki Ta |
| Chatusra | 4 | `l4` | Tha Ka Dhi Mi |
| Khanda | 5 | `l5` | Tha Ka Tha Ki Ta |
| Misra | 7 | `l7` | Tha Ki Ta Tha Ka Dhi Mi |
| Sankeerna | 9 | `l9` | Tha Ka Dhi Mi Tha Ka Tha Ki Ta |

### Extended Anga Symbols (108-Tala System)

| Anga | Symbol | Aksharas |
|------|--------|----------|
| Anudrutam | `U` | 1 |
| Druta | `O` | 2 |
| Laghu | `l` | 3–9 (jaati-dependent) |
| Guru | `8` | 8 |
| Plutam | `)` | 12 |
| Kakapadam | `+` | 16 |

### Suladi Sapta Talas — Anga Structure

| Tala Name | Anga Pattern | Aksharas (Chatusra) |
|-----------|-------------|---------------------|
| Dhruva | `l O l l` | 14 |
| Matya | `l O l` | 10 |
| Rupaka | `O l` | 6 |
| Jhampa | `l U O` | 7 |
| Triputa | `l O O` | 7 → **Adi Tala** (most common) |
| Ata | `l l O O` | 14 |
| Eka | `l` | 4 |

### Chapu Talas (Non-Anga Talas)

| Name | Beats | Pattern | Mnemonic |
|------|-------|---------|----------|
| Thisra Chapu | 3 | 1+2 | Tha-Ki-Ta |
| Khanda Chapu | 5 | 2+3 | Tha-Ka-Tha-Ki-Ta |
| Misra Chapu | 7 | 3+4 | Tha-Ki-Ta-Tha-Ka-Dhi-Mi |
| Sankeerna Chapu | 9 | 4+5 | Tha-Ka-Dhi-Mi-Tha-Ka-Tha-Ki-Ta |

### Notation Example — Adi Tala (Chatusra Triputa)

```
tala: Triputa | jaati: Chatusra | aksharas: 8
anga: l4 O O  →  | S R G M | P D | N S' |
```

---

## 6. FULL DELIVERABLES ROADMAP

### Phase 1 — Core Specification (Week 1–2)
- [ ] **SPEC.md** — Complete notation standard (swaras, gamakas, talas)
- [ ] **PHONETICS.md** — Full AI phonetic encoding table
- [ ] **GAMAKAS.md** — 15 gamakas with symbols, AI vectors, examples
- [ ] **TALAS.md** — Suladi Sapta Talas + Chapu + 108 extended system
- [ ] **todo.md** — THIS FILE ✅

### Phase 2 — TypeScript/JS Library (Week 3–5)
- [ ] **Parser module** — Parse ASCII notation string → AST (Abstract Syntax Tree)
  - Lexer: tokenize swaras, gamakas, tala markers
  - Parser: build phrase tree with timing
- [ ] **Renderer module** — AST → SVG output (based on carnot architecture)
  - Swara boxes with gamaka symbols
  - Tala line rendering
  - Multi-octave staff rendering
- [ ] **Gamaka engine** — Symbol → pitch contour mapping
  - `GMK_KAMP`: sine oscillation function
  - `GMK_EJRU`: linear interpolation (ascending)
  - `GMK_IJRU`: linear interpolation (descending)
- [ ] **Tala engine** — Beat pattern generator
  - Anga sequencer (U, O, l)
  - Tempo (BPM) mapper

### Phase 3 — Python Package (Week 4–6)
- [ ] **`raganotate` package** structure:
  ```
  raganotate/
  ├── __init__.py
  ├── swara.py         # Swara + Swarasthana classes
  ├── gamaka.py        # Gamaka types + AI feature vectors
  ├── tala.py          # Tala + Anga system
  ├── parser.py        # ASCII notation → Python objects
  ├── renderer.py      # Python → MIDI / LilyPond / MusicXML
  ├── ai_encoder.py    # Notation → AI-ready tokens
  └── dataset.py       # Dataset utilities for ML training
  ```
- [ ] **MIDI export** — Map swaras to MIDI notes with gamaka pitch bends
- [ ] **AI tokenizer** — Encode notation as token sequences for LLM training

### Phase 4 — Web UI (Week 6–8)
- [ ] **Live notation editor** (HTML + CodeMirror)
  - Syntax highlighting for notation
  - Real-time SVG preview
- [ ] **Gamaka visualizer** — Pitch contour graph per phrase
- [ ] **Tala beat clock** — Visual beat counter with anga markers
- [ ] **Raga selector** — Auto-validate notes against raga grammar

### Phase 5 — GitHub Repository (Week 8–9)
- [ ] Create repo: `github.com/jags111/RagaNotate`
- [ ] Setup `README.md` with notation quickstart guide
- [ ] Add `examples/` folder with 5–10 classic compositions
- [ ] CI/CD: GitHub Actions for testing TypeScript + Python

### Phase 6 — Dataset & AI Training (Week 9–12)
- [ ] Annotate 50+ Carnatic compositions in the notation format
- [ ] Build gamaka classification dataset (JSON)
- [ ] Create `train/test` split for ML experiments
- [ ] Publish dataset to HuggingFace datasets

---

## 7. REPOSITORY STRUCTURE

```
RagaNotate/
│
├── README.md                  # Quickstart guide
├── SPEC.md                    # Full notation specification
├── todo.md                    # This file
│
├── spec/
│   ├── PHONETICS.md           # 16 swarasthana phonetics
│   ├── GAMAKAS.md             # 15 gamakas reference
│   └── TALAS.md               # Tala system reference
│
├── packages/
│   ├── js/                    # TypeScript/JS library
│   │   ├── src/
│   │   │   ├── lexer.ts
│   │   │   ├── parser.ts
│   │   │   ├── renderer.ts
│   │   │   ├── gamaka.ts
│   │   │   └── tala.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   └── python/                # Python package
│       ├── raganotate/
│       │   ├── swara.py
│       │   ├── gamaka.py
│       │   ├── tala.py
│       │   ├── parser.py
│       │   ├── renderer.py
│       │   └── ai_encoder.py
│       ├── tests/
│       └── setup.py
│
├── web/                       # Web UI
│   ├── index.html
│   ├── editor.html
│   └── assets/
│
├── examples/                  # Sample compositions
│   ├── ganarajena.txt
│   ├── sri_ganesha.txt
│   └── vathapi.txt
│
└── dataset/                   # AI training data
    ├── annotated/
    └── gamaka_labels.json
```

---

## 8. IMPLEMENTATION PHASES

### Quick Start — Notation Format Summary

```
# Full Notation Quick Reference

OCTAVE:   .s .r .g .m .p .d .n  |  S R G M P D N  |  S' R' G' M' P' D' N'
DURATION: S (1) | S; (2) | S: (0.5) | S:: (0.25)
BEAT:     | = beat marker | , = visible gap | - = rest | _ = invisible gap

GAMAKAS:  ~~ (kampita) | ^ (slide up) | v (slide down)
          * (nokku/stress) | (^) (sphurita) | (v) (pratyaghata)

TALA:     l4 = Laghu Chatusra | O = Dhrutam | U = Anudhrutam
          Adi = l4 O O = 8 aksharas

EXAMPLE:
  tala: Adi | jaati: Chatusra | speed: madhyama
  | S R~~ G M | P^D N S' | N v D P | M G R S |
  | ya  -  mu  - | na  - ka  - | la  - ya  - | di  - pa  - |
```

---

## 9. REFERENCES

### Core Architecture
- [srikumarks/carnot](https://github.com/srikumarks/carnot) — JS SVG rendering engine for Carnatic notation
- [ragasangrah.com](https://ragasangrah.com/) — Core integration reference, gamaka examples

### Notation & Theory
- [iSargam (Springer 2016)](https://link.springer.com/article/10.1186/s13636-016-0083-z) — Unicode-based Indian notation encoding
- [karnatik.com/symbols](https://www.karnatik.com/symbols.shtml) — Standard notation symbols
- [saayujya.com — Gamaka Notation](https://saayujya.com/index.php/2019/12/03/gamaka-notation/)

### Tala System
- [Upbeat Labs — Tala Primer](https://www.upbeatlabs.com/2017/01/17/a-primer-for-carnatic-talas/)
- [HCL Concerts — Common Talas](https://www.hclconcerts.com/blogs/common-talas-in-carnatic-music/)
- [carnaticmusicexams.in — 35 Talas](https://carnaticmusicexams.in/2018/06/19/the-scheme-of-35-talas/)
- [The Mystic Keys — Talas & Rhythms](https://themystickeys.com/talas-and-rhythms-mastering-the-beat-in-carnatic-music/)
- [Acharyanet — All About Talas](https://www.acharyanet.com/all-about-talas-in-carnatic-music/)
- [Artium Academy — Tala Philosophy](https://artiumacademy.com/blogs/silent-language-of-taal-in-music-exploring-philosophical-underpinnings-of-tala-in-indian-classical-music/)
- [karnatik.com/ctaala](https://www.karnatik.com/ctaala.shtml)

### Carnatic AI / ML Projects
- [sarayusapa/sam-carnatic](https://github.com/sarayusapa/sam-carnatic)
- [NK2511/Carnatic-Annotator](https://github.com/NK2511/Carnatic-Annotator)
- [PradeepaK1/Carnatic-Notes-Predictor](https://github.com/PradeepaK1/Carnatic-Notes-Predictor-for-audio-files)
- [AadarshLN/Audio-Classification-Carnatic](https://github.com/AadarshLN/Audio-Classification-in-Carnatic-Classical-Music)
- [VikramVasudevan/carnatic-music-ai](https://github.com/VikramVasudevan/carnatic-music-ai)
- [TISMIR22-Carnatic/carnatic-pitch-patterns](https://github.com/TISMIR22-Carnatic/carnatic-pitch-patterns)
- [abiramigiri/Raga-Detection-Script](https://github.com/abiramigiri/Raga-Detection-Script)

### Audio & Music Generation (Integration Reference)
- [fspecii/HeartMuLa-Studio](https://github.com/fspecii/HeartMuLa-Studio)
- [Alvin-Liu/suno-music-generator](https://github.com/Alvin-Liu/suno-music-generator)
- [asigalov61/Tegridy-MIDI-Dataset](https://github.com/asigalov61/Tegridy-MIDI-Dataset)
- [surikov/riffshare](https://github.com/surikov/riffshare)
- [hlorenzi/musicode](https://github.com/hlorenzi/musicode)

### Core Papers & Texts
- *Sangita Sampradaya Pradarshini* — Subbarama Dikshitar
- *Natya Shastra* — Bharata Muni

---

## ✅ TASK CHECKLIST

- [x] Define octave notation standard (Jags' standard adopted)
- [x] Map all 16 swarasthanas with phonetic suffixes
- [x] Define 15 gamakas with AI tokens + pitch curve types
- [x] Document Suladi Sapta Tala anga system
- [x] Document Chapu talas
- [x] Create repository structure
- [x] Create workflow chart (HTML)
- [ ] Implement TypeScript lexer/parser
- [ ] Implement Python raganotate package
- [ ] Build web UI editor
- [ ] Create GitHub repo: github.com/jags111/RagaNotate
- [ ] Annotate 50+ example compositions
- [ ] Build AI training dataset
- [ ] Publish Python package to PyPI
- [ ] Publish TypeScript package to npm

---

*Last updated: 2026-03-10 | by Jags (jags111) | v0.1.0 | [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)*
