# 🎵 RagaNotate

> **Full-Stack Carnatic Music Notation Engine**
> A human-readable, AI-compatible notation system for Carnatic classical music.

[![Version](https://img.shields.io/badge/version-0.2.0-gold)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-Active%20Development-brightgreen)](#roadmap)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](packages/python/)
[![TypeScript](https://img.shields.io/badge/typescript-5.x-blue)](packages/js/)
[![Author](https://img.shields.io/badge/author-jags111-purple)](https://github.com/jags111)

---

## What Is RagaNotate?

**RagaNotate** bridges human Carnatic musicians and AI/ML systems. It defines a clean ASCII notation format for swaras, gamakas, and talas — then provides tools to parse, render, play, and export that notation.

- **ASCII notation format** — human-readable, version-control friendly
- **Python package** (`raganotate`) — parse, export MIDI with Just Intonation tuning, tokenize for AI/ML
- **TypeScript library** — identical features for browser and Node.js environments
- **Web UI** — open `web/raganotate_editor.html` in any browser, no server needed
- **AI dataset** — annotated Carnatic compositions for ML training

---

## ⚡ Quick Start — Try It in 30 Seconds

**No installation required.** Open the self-contained web editor:

```
web/raganotate_editor.html
```

Just double-click the file in your file explorer (or drag it into Chrome/Firefox). You'll get:

**Three tabs:**

- **Notation Editor** — live CodeMirror editor → real-time SVG preview, tala beat clock, shruti drone, ▶ Play with gamaka synthesis, raga-aware highlighting, dark/light theme
- **Geetham / Composition Editor** — add composition header (title, raga, tala, arohanam, avarohanam), section blocks (Pallavi / Anupallavi / Charanam), per-bar notation + aligned lyrics, SVG preview per section, ▶ Play Geetham, ⬇ Export SVG. Pre-loaded with Jayakaru Geetam (Dhanyasi, Chaturashra Dhruvam)
- **Raga Reference** — searchable table of 30+ ragas with arohanam/avarohanam, vadi/samvadi, parent melakarta

**Type this into the editor and press ▶ Play:**

```
| S R~ G+ M | P D N+ S' | N+ D P M | G+ R S ||
```

That's the ascending and descending Shankarabharanam scale in Adi Tala.

---

## Notation Format

### Swaras

```
MANDRA (low):   .S  .r  .R  .g  .G+ .m  .M  .P  .d  .D  .n  .N+
MADHYA (mid):    S   r   R   g   G+  m   M   P   d   D   n   N+
TARA (high):    S'  r'  R'  g'  G+' m'  M'  P'  d'  D'  n'  N+'
```

### Duration

| Symbol | Meaning |
|--------|---------|
| `S`    | 1 akshara (one beat) |
| `S;`   | 2 aksharas (double) |
| `S:`   | ½ akshara |
| `S::`  | ¼ akshara |

### Beat Markers

| Symbol | Meaning |
|--------|---------|
| `\|`   | Bar / beat boundary |
| `\|\|` | Section end |
| `,`    | Half-beat gap |
| `-`    | Rest / silence |

### Gamakas

| Symbol | Gamaka | Description |
|--------|--------|-------------|
| `~`    | Kampita | Oscillating vibrato |
| `/`    | Jaru ascending | Slide upward to note |
| `\`    | Jaru descending | Slide downward to note |
| `^`    | Sphurita | Grace-note bend at onset |
| `v`    | Pratyaghata | Grace-note bend downward |
| `w`    | Andola | Wide oscillation |
| `*`    | Nokku | Stress accent |

### Full Example

```
| S  R~  G+  M   | P   D   N+  S'  ||   ← Shankarabharanam ascending
| S' N+\ D   P   | M   G+  R   S   ||   ← descending with jaru
| S  R~  G+/ M   | P^  D   N+\ S' ||    ← with gamakas
```

---

## The 12 Swarasthana Positions

Carnatic music defines **16 swarasthana names**, but there are only **12 unique pitch positions** because 4 pairs of names share the same frequency (enharmonic equivalents). The 2 achala (immovable) swaras — Sa and Pa — are fixed. The remaining 10 positions are chala (movable).

All frequencies use standard 5-limit **Just Intonation** (JI), not equal temperament.

| Pos | Symbol | Full Name | Enharmonic Alias | Ratio | Hz @ Sa=240 |
|-----|--------|-----------|-----------------|-------|-------------|
| 1  | **S**  | Shadjam | — (achala) | 1/1 | 240.00 |
| 2  | **r**  | Suddha Rishabham (R1) | — | 16/15 | 256.00 |
| 3  | **R**  | Chatusruti Rishabham (R2) | = G1 Suddha Gandharam | 9/8 | 270.00 |
| 4  | **g**  | Shatshruti Rishabham (R3) | = G2 Sadharana Gandharam | 6/5 | 288.00 |
| 5  | **G+** | Antara Gandharam (G3) | — | 5/4 | 300.00 |
| 6  | **m**  | Suddha Madhyamam (M1) | — | 4/3 | 320.00 |
| 7  | **M**  | Prati Madhyamam (M2) | — | 45/32 | 337.50 |
| 8  | **P**  | Panchamam | — (achala) | 3/2 | 360.00 |
| 9  | **d**  | Suddha Dhaivatam (D1) | — | 8/5 | 384.00 |
| 10 | **D**  | Chatusruti Dhaivatam (D2) | = N1 Suddha Nishadam | 5/3 | 400.00 |
| 11 | **n**  | Shatshruti Dhaivatam (D3) | = N2 Kaisika Nishadam | 9/5 | 432.00 |
| 12 | **N+** | Kakali Nishadam (N3) | — | 15/8 | 450.00 |
| — | **S'** | Tara Shadjam | higher octave Sa | 2/1 | 480.00 |
| — | **.S** | Mandra Shadjam | lower octave Sa | 1/2 | 120.00 |

**The 4 enharmonic pairs** (same pitch, two Melakarta names):

| Position | R-name | G/D/N-name | Ratio | Hz |
|----------|--------|------------|-------|----|
| 3 | Chatusruti Ri (R2) | Suddha Ga (G1) | 9/8 | 270.00 |
| 4 | Shatshruti Ri (R3) | Sadharana Ga (G2) | 6/5 | 288.00 |
| 10 | Chatusruti Dha (D2) | Suddha Ni (N1) | 5/3 | 400.00 |
| 11 | Shatshruti Dha (D3) | Kaisika Ni (N2) | 9/5 | 432.00 |

> **Why Just Intonation?** Equal temperament (piano tuning) divides the octave into 12 equal steps. Carnatic music uses pure harmonic ratios derived from the overtone series — these create consonant intervals that sound distinctly different from Western tuning. The differences are not errors; they are the characteristic sound of the system.

---

## Python Package

### Install

```bash
cd packages/python
pip install -e .
pip install MIDIUtil   # for MIDI export (capital M and U)
```

### Parse and inspect notation

```python
from raganotate import parse_notation
from raganotate.swara import SWARASTHANAS

# See all 12 swarasthana positions with their JI ratios
for sym, sw in SWARASTHANAS.items():
    print(f"  {sym:3s}  {sw.ratio}  =  {float(sw.ratio)*240:.2f} Hz")

# Parse a notation string
ast = parse_notation("| S R~ G+ M | P D N+ S' ||", tala="Adi")
print(ast)
```

### Export MIDI

```python
from raganotate import parse_notation
from raganotate.midi_generator import ast_to_midi

ast = parse_notation("| S R G+ M | P D N+ S' | N+ D P M | G+ R S ||", tala="Adi")
ast_to_midi(ast, "scale.mid", sa_hz=240.0, bpm=72.0)
# Opens in GarageBand, Logic, Ableton, MuseScore, LMMS, VLC…
```

See [docs/midi_test.md](docs/midi_test.md) for a full MIDI usage guide.

### AI / HuggingFace tokenization

```python
from raganotate import parse_notation
from raganotate.ai_encoder import ast_to_token_sequence, ast_to_dataset_record

ast = parse_notation("| S R G+ M | P D N+ S' ||", tala="Adi")
tokens = ast_to_token_sequence(ast)
record = ast_to_dataset_record(ast, title="Sa Re Ga Ma scale", raga="Shankarabharanam")
```

---

## TypeScript / JavaScript Library

```typescript
import { parse } from './src/parser';
import { renderSVG } from './src/renderer';
import { TalaEngine, TALAS } from './src/tala';

// Parse notation
const ast = parse('| S R~ G+ M | P D N+ S\' ||');

// Render to SVG string
const svg = renderSVG(ast);
document.getElementById('preview').innerHTML = svg;

// Run tala beat clock
const engine = new TalaEngine(TALAS['Adi'], 72);
engine.onBeat = (evt) => console.log(evt.label, evt.isSam ? '← SAM' : '');
engine.start();
```

```bash
cd packages/js
npm install
npm run build   # compiles TypeScript → dist/
```

---

## Repository Structure

```
RagaNotate/
├── README.md                    ← You are here
├── SPEC.md                      ← Full notation specification
├── ARCHITECTURE.md              ← System design
├── CHANGELOG.md                 ← Full version history
├── SESSION_STATE.md             ← Session recovery guide (for AI-assisted dev)
├── checkpoint.sh                ← Run at session end to create local bundle backup
├── .gitattributes               ← LF/CRLF rules
│
├── packages/
│   ├── python/                  ← pip-installable Python package
│   │   ├── setup.py             ← version = "0.1.5"
│   │   ├── requirements.txt
│   │   └── raganotate/
│   │       ├── __init__.py
│   │       ├── swara.py         ← 12-position swarasthanas, JI ratios
│   │       ├── gamaka.py        ← 15 gamakas + pitch contour functions
│   │       ├── tala.py          ← TalaEngine (all 8 talas + chapu)
│   │       ├── parser.py        ← ASCII notation → NotationAST
│   │       ├── lyrics_mapper.py ← align lyrics to swaras
│   │       ├── ai_encoder.py    ← AST → token sequences + HF dataset records
│   │       ├── raga_grammar.py  ← raga rules + validation
│   │       └── midi_generator.py← AST → MIDI with JI pitch bends
│   │
│   └── js/                      ← TypeScript/JS library (Node + browser)
│       ├── package.json
│       ├── tsconfig.json
│       └── src/
│           ├── types.ts         ← all interfaces
│           ├── lexer.ts
│           ├── parser.ts        ← full AST builder
│           ├── renderer.ts      ← AST → SVG
│           ├── gamaka.ts
│           ├── tala.ts          ← TalaEngine class
│           └── audio.ts
│
├── web/
│   ├── raganotate_editor.html   ← Self-contained live editor v0.2.0 — three-tab layout
│   └── swarasthana_explorer.html← Interactive 16-swarasthana reference with playback
│
├── docs/
│   └── midi_test.md             ← How to test MIDI export locally
│
├── dataset/
│   ├── sawarsthanam.xlsx        ← Swarasthana reference spreadsheet
│   └── annotated/               ← HuggingFace dataset (compositions in JSON)
│
└── data/, examples/, spec/      ← Additional assets
```

---

## Roadmap

| Version | What | Status |
|---------|------|--------|
| **v0.1.0** | Core specification + Python swara/tala engine | ✅ Done |
| **v0.1.1** | Spec refinement + lyrics-to-notation architecture | ✅ Done |
| **v0.1.2** | TS parser + renderer + SVG output + ai_encoder.py | ✅ Done |
| **v0.1.3** | Swarasthana ratio audit + JI correction | ✅ Done |
| **v0.1.4** | Web UI (raga highlighting, playback, shruti drone) + TalaEngine TS | ✅ Done |
| **v0.2.0** | Canonical notation + 72 Melakarta DB + Geetham Editor + swarasthana_explorer | ✅ Done |
| v0.3.0 | MIDI export UI + HuggingFace dataset (10+ compositions) | 🔲 Next |
| v0.4.0 | PyPI + npm publish | 🔲 Planned |
| v1.0.0 | Full AI training dataset + model | 🔲 Planned |

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## Ragas Included (Web Editor — 30+ in dropdown)

Popular Janya ragas and key Melakartas are selectable in the editor. A selection:

| Raga | Arohanam | Parent Mela |
|------|----------|------------|
| Hamsadhvani | S R G+ P N+ | 29 Shankarabharanam |
| Shankarabharanam | S R G+ m P D N+ | 29 (melakarta) |
| Kalyani / Mechakalyani | S R G+ M P D N+ | 65 (melakarta) |
| Bhairavi | S r g m P d n | 20 Natabhairavi |
| Mohanam | S R G+ P D | 28 Harikambhoji |
| Bilahari | S R G+ P D N+ | 29 Shankarabharanam |
| Todi / Subhapantuvarali | S r g m P d N+ | 45 Shubhapanthuvarali |
| Kharaharapriya | S R g m P D n | 22 (melakarta) |
| Mayamalavagowla | S r G+ m P d N+ | 15 (melakarta) |
| Hanumatodi | S r g m P d N+ | 8 (melakarta) |
| Dhanyasi | S g m P n | 8 Hanumatodi |
| Charukeshi | S R G+ m P d n | 26 Charukeshi |
| Natabhairavi | S R g m P d n | 20 (melakarta) |

Full 72 Melakarta reference: [References/RAGA_DATABASE.md](../References/RAGA_DATABASE.md)

---

## Talas Supported

| Tala | Anga Pattern | Beats |
|------|-------------|-------|
| Adi | Laghu(4) + 2×Drutam | 8 |
| Rupaka | Drutam + Laghu(2) | 6 |
| Misra Chapu | 3+2+2 | 7 |
| Khanda Chapu | 2+3 | 5 |
| Eka | Laghu(4) | 4 |
| Jhampai | Laghu(3) + Anu + Drutam | 10 |
| Triputa | Laghu(3) + 2×Drutam | 7 |
| Matya | Laghu(4) + Drutam + Laghu(4) | 14 |

---

## References

- [srikumarks/carnot](https://github.com/srikumarks/carnot) — SVG rendering engine for Carnatic notation
- [ragasangrah.com/gamakas](https://ragasangrah.com/gamakas) — Gamaka reference
- [iSargam (Springer 2016)](https://link.springer.com/article/10.1186/s13636-016-0083-z) — Unicode-based Indian notation encoding
- [karnatik.com/symbols](https://www.karnatik.com/symbols.shtml) — Standard notation symbols
- *Sangita Sampradaya Pradarshini* — Subbarama Dikshitar (primary classical authority on raga grammars)
- *Natya Shastra* — Bharata Muni

---

## Author

**Jags** · [@jags111](https://github.com/jags111) · [info@revsmartasia.com](mailto:info@revsmartasia.com)

---

## License

MIT © 2026 Jags (jags111). See [LICENSE](LICENSE).
