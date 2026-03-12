# RagaNotate — System Architecture

> **Version:** 0.1.1
> **Author:** Jags (jags111) · [github.com/jags111](https://github.com/jags111)
> **Repository:** [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)

---

## System Overview

RagaNotate converts **song lyrics** and **notation input** into:
- Visual notation (SVG)
- Playable audio (MIDI / Web Audio / synthesis)
- AI-ready token sequences (for ML/LLM training)

---

## Full Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
│                                                                 │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐     │
│  │ Raw Lyrics    │   │ ASCII         │   │ Existing MIDI │     │
│  │ (text/UTF-8)  │   │ Notation      │   │ / Audio File  │     │
│  └───────┬───────┘   └───────┬───────┘   └───────┬───────┘     │
└──────────┼───────────────────┼───────────────────┼─────────────┘
           │                   │                   │
           ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                      PARSING LAYER                               │
│                                                                  │
│  ┌──────────────────┐     ┌───────────────────────────────────┐  │
│  │ LyricsMapper     │     │ NotationLexer → NotationParser    │  │
│  │                  │     │                                   │  │
│  │ • Syllabify text │     │ • Tokenize swara symbols          │  │
│  │ • Map syllables  │     │ • Tokenize gamaka markers         │  │
│  │   to swaras      │     │ • Tokenize tala markers           │  │
│  │ • Assign gamakas │     │ • Build Abstract Syntax Tree      │  │
│  │   from raga      │     │   (AST) of the phrase             │  │
│  └────────┬─────────┘     └─────────────┬─────────────────────┘  │
│           │                             │                        │
│           └──────────────┬──────────────┘                        │
│                          │                                        │
│                          ▼                                        │
│              ┌───────────────────────┐                            │
│              │  Notation AST         │                            │
│              │  ─────────────────    │                            │
│              │  SwaraNode            │                            │
│              │    .symbol (S, R, G…) │                            │
│              │    .octave (lo/md/hi) │                            │
│              │    .variant (1/2/3)   │                            │
│              │    .duration (beats)  │                            │
│              │    .gamaka (GamakaNode│                            │
│              │    .lyric  (syllable) │                            │
│              │  TalaNode             │                            │
│              │    .name (Adi, etc.)  │                            │
│              │    .aksharas (8)      │                            │
│              │    .angas [l4, O, O]  │                            │
│              └───────────┬───────────┘                            │
└──────────────────────────┼────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┬─────────────────────┐
           │               │               │                     │
           ▼               ▼               ▼                     ▼
┌──────────────┐  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐
│  SVG         │  │  MIDI          │  │  Audio       │  │  AI Encoder │
│  Renderer    │  │  Generator     │  │  Synthesizer │  │             │
│              │  │                │  │              │  │             │
│ • Swara boxes│  │ • Hz → MIDI    │  │ • Direct     │  │ • Token seq │
│ • Gamaka     │  │   note mapping │  │   sine/FM    │  │ • 6D gamaka │
│   symbols    │  │ • Pitch bends  │  │   synthesis  │  │   vectors   │
│ • Tala grid  │  │   for gamakas  │  │ • Gamaka     │  │ • Raga      │
│ • Lyric text │  │ • Tempo / BPM  │  │   contours   │  │   grammar   │
│ • Multi-     │  │ • Export .mid  │  │ • Web Audio  │  │   tokens    │
│   octave     │  │                │  │   API (TS)   │  │ • HuggingFace│
│   staff      │  │                │  │ • scipy (Py) │  │   dataset   │
└──────────────┘  └────────────────┘  └──────────────┘  └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────┐
│              OUTPUT LAYER                   │
│  .svg  │  .mid  │  .wav/.mp3  │  .json      │
│  Web UI editor  │  HuggingFace dataset      │
└─────────────────────────────────────────────┘
```

---

## Module Breakdown

### Python Package: `raganotate`

```
raganotate/
├── __init__.py          # Public API surface
├── swara.py             # Swara + 16 Swarasthana definitions
├── gamaka.py            # 15 Gamakas + notation symbols + AI vectors
├── tala.py              # Tala + Anga system (Suladi Sapta + Chapu)
├── parser.py            # ASCII notation string → AST
├── lyrics_mapper.py     # Lyrics text → notation alignment
├── notation_generator.py# AST → ASCII notation string
├── renderer.py          # AST → SVG / LilyPond / MusicXML
├── midi_generator.py    # AST → MIDI (.mid) with pitch bends
├── audio_synth.py       # AST → audio waveform (numpy/scipy)
├── ai_encoder.py        # AST → AI token sequences
├── raga_grammar.py      # Raga definitions + swara validation
└── dataset.py           # Dataset utilities for ML training
```

### TypeScript Package: `@jags111/raganotate`

```
packages/js/src/
├── types.ts             # All shared interfaces & type definitions
├── lexer.ts             # Tokenizer: string → Token[]
├── parser.ts            # Token[] → AST (SwaraNode, TalaNode, etc.)
├── renderer.ts          # AST → SVG string
├── gamaka.ts            # Gamaka symbol map + pitch contour functions
├── tala.ts              # Tala definitions + beat pattern generator
├── audio.ts             # Web Audio API synthesis engine
├── midiExport.ts        # AST → MIDI binary (browser download)
└── index.ts             # Package entry point
```

---

## Data Flow — Lyrics to Audio (Step by Step)

### Step 1 — Input
```
Input lyrics:    "Vathapi Ganapatim Bhaje"
Selected raga:   Hamsadhvani
Selected tala:   Adi (8 beats)
Sa frequency:    240 Hz
```

### Step 2 — Syllabify
```python
syllables = ["Va", "tha", "pi", "Ga", "na", "pa", "tim", "Bha", "je"]
```

### Step 3 — Raga Grammar (Hamsadhvani: S R G P N)
```python
# Valid swaras: S, R, G3, P, N3 only (pentatonic)
# Arohana: S R G P N S'
# Avarohana: S' N P G R S
```

### Step 4 — Lyrics Mapper → Notation
```
Va   tha  pi   Ga   na   pa   tim  Bha  je
S    R    G    P    N    S'   N    P    G
```

### Step 5 — Gamaka Assignment (from raga conventions)
```
S    R~   G^   P    N    S'   N\   P    G~
```

### Step 6 — Tala Alignment (Adi, 8 beats)
```
| S R~ G^ P | N S' N\ P | G~ R S ,  |
  beat 1      beat 2      beat 3
```

### Step 7 — AST Built
```json
{
  "tala": {"name": "Adi", "aksharas": 8, "angas": ["l4","O","O"]},
  "phrases": [
    {"swara": "S", "octave": "madhya", "duration": 1, "gamaka": null, "lyric": "Va"},
    {"swara": "R", "octave": "madhya", "duration": 1, "gamaka": "GMK_KAMP", "lyric": "tha"},
    ...
  ]
}
```

### Step 8 — Output Selection

| Output | Module | Format |
|--------|--------|--------|
| Visual notation | `renderer.py` / `renderer.ts` | `.svg` |
| MIDI file | `midi_generator.py` / `midiExport.ts` | `.mid` |
| Audio waveform | `audio_synth.py` | `.wav` |
| Web playback | `audio.ts` (Web Audio API) | browser |
| AI training data | `ai_encoder.py` | `.json` |

---

## Gamaka Audio Rendering

Each gamaka maps to a mathematical function over time `t ∈ [0, duration]`:

| Gamaka | Symbol | Pitch Function f(t) |
|--------|--------|---------------------|
| Ahata | *(none)* | `f(t) = target_hz` (constant) |
| Kampita `~` | GMK_KAMP | `f(t) = target_hz * (1 + A·sin(2π·rate·t))` |
| Jaru up `/` | GMK_EJRU | `f(t) = onset_hz + (target_hz - onset_hz)·(t/dur)` |
| Jaru down `\` | GMK_IJRU | `f(t) = onset_hz - (onset_hz - target_hz)·(t/dur)` |
| Sphurita `^` | GMK_SPHU | `f(t) = target_hz*(1+ε) → target_hz` (brief upper touch) |
| Pratyaghata `v` | GMK_PRAT | `f(t) = target_hz*(1-ε) → target_hz` (brief lower touch) |
| Andola `w` | GMK_ANDO | `f(t) = target_hz + A·sin(2π·rate·t)` (wide, slow) |
| Tribhinna `tr` | GMK_TRIB | Three-point interpolation across adjacent swaras |
| Vibrato `vib` | GMK_VIB  | Kampita with wider amplitude: `A = 0.04` vs `0.02` |

---

## Tala Beat Clock

```
Adi Tala (l4 O O = 8 aksharas):

Beat:   1    2    3    4  |  5  6  |  7  8
Anga:   ←── Laghu (l4) ──→  ← O → ← O →
Hand:   clap +1 +2 +3      dn up  dn up
```

MIDI timing: `1 akshara = (60 / BPM) seconds`

---

## Raga Grammar Validator

Each raga defines:
- **Arohana** (ascending scale): permitted swaras ascending
- **Avarohana** (descending scale): permitted swaras descending
- **Vadi** (principal swara) + **Samvadi** (secondary)
- **Gamaka rules**: which gamakas are idiomatic per swara

Example — Hamsadhvani:
```python
HAMSADHVANI = {
    "arohana":   ["S", "R", "G3", "P", "N3", "S'"],
    "avarohana": ["S'", "N3", "P", "G3", "R", "S"],
    "vadi": "G3", "samvadi": "N3",
    "gamaka_rules": {
        "G3": ["GMK_KAMP", "GMK_SPHU"],
        "N3": ["GMK_KAMP", "GMK_IJRU"],
        "R":  ["GMK_EJRU"],
    }
}
```

---

## Integration References

| Purpose | Library / Repo |
|---------|---------------|
| SVG notation rendering | [srikumarks/carnot](https://github.com/srikumarks/carnot) |
| Raga/gamaka reference | [ragasangrah.com](https://ragasangrah.com/) |
| MIDI dataset | [asigalov61/Tegridy-MIDI-Dataset](https://github.com/asigalov61/Tegridy-MIDI-Dataset) |
| Web audio synthesis | [hlorenzi/musicode](https://github.com/hlorenzi/musicode) |
| Carnatic pitch ML | [TISMIR22-Carnatic/carnatic-pitch-patterns](https://github.com/TISMIR22-Carnatic/carnatic-pitch-patterns) |
| Raga detection | [abiramigiri/Raga-Detection-Script](https://github.com/abiramigiri/Raga-Detection-Script) |
| Carnatic AI | [VikramVasudevan/carnatic-music-ai](https://github.com/VikramVasudevan/carnatic-music-ai) |
| Music generation | [Alvin-Liu/suno-music-generator](https://github.com/Alvin-Liu/suno-music-generator) |

---

*RagaNotate ARCHITECTURE v0.1.1 · 2026-03-10 · [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)*
