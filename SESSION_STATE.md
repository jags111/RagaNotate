# RagaNotate — Session State & Recovery Guide

> **Last updated:** 2026-03-12
> **Current version:** v0.1.4
> **GitHub:** https://github.com/jags111/RagaNotate
> **Owner:** Jags · info@revsmartasia.com · github.com/jags111

---

## How to Resume a Session

If context is lost, share this file with Claude and say:
> "Resume RagaNotate development. Read SESSION_STATE.md first."

---

## What This Project Is

**RagaNotate** — A full-stack Carnatic music notation system.

A domain-specific language (ASCII notation) + parser + SVG renderer + MIDI exporter + Web UI + AI tokenizer for Carnatic music compositions.

- Notation: `| S R~ G+ M | P D N+ S' ||` (ASCII, human-readable)
- Python library: parse, render SVG, export MIDI, encode for AI/ML
- TypeScript library: same features for browser/Node.js
- Web UI: live CodeMirror editor → real-time SVG preview + tala beat clock + shruti drone

---

## Repository Structure

```
RagaNotate/
├── SPEC.md                    ← Notation language specification
├── ARCHITECTURE.md            ← System design
├── CHANGELOG.md               ← Full version history
├── README.md                  ← GitHub landing page
├── todo.md                    ← Original roadmap
├── SESSION_STATE.md           ← THIS FILE — session recovery
├── checkpoint.sh              ← Run at session end to save bundle
├── .gitattributes             ← LF/CRLF line ending rules
├── .gitignore
│
├── packages/
│   ├── python/
│   │   ├── setup.py           ← version="0.1.4"
│   │   ├── requirements.txt   ← all deps including MIDIUtil>=1.2.1
│   │   └── raganotate/
│   │       ├── __init__.py    ← __version__ = "0.1.4"
│   │       ├── swara.py       ← 16 swarasthanas, JI ratios (v0.1.3 corrected)
│   │       ├── gamaka.py      ← 15 gamakas + pitch contour functions
│   │       ├── tala.py        ← TalaEngine, all 8 talas + chapu
│   │       ├── parser.py      ← ASCII notation → NotationAST
│   │       ├── lyrics_mapper.py
│   │       ├── ai_encoder.py  ← AST → token sequences, feature vectors, HF dataset
│   │       ├── raga_grammar.py
│   │       └── midi_generator.py  ← AST → MIDI with JI pitch bends
│   │
│   └── js/
│       ├── package.json       ← "version": "0.1.4"
│       ├── tsconfig.json
│       └── src/
│           ├── types.ts       ← all interfaces
│           ├── lexer.ts
│           ├── parser.ts      ← full AST builder
│           ├── renderer.ts    ← AST → SVG
│           ├── gamaka.ts
│           ├── tala.ts        ← TalaEngine class (full, v0.1.4)
│           └── audio.ts
│
├── web/
│   └── raganotate_editor.html ← Self-contained live editor (1318 lines)
│
├── dataset/
│   ├── sawarsthanam.xlsx      ← Swarasthana reference (v0.1.3 corrected)
│   └── annotated/             ← HuggingFace dataset (TODO: 10+ compositions)
│
├── docs/
│   └── midi_test.md           ← How to test MIDI export locally
│
├── data/, examples/, spec/    ← Other assets
```

---

## Critical Technical Facts

### Notation Syntax
```
| S  R~ G+ M  | P  D  N+/ S' |    ← standard bar notation
  ^  ^   ^  ^    ^  ^   ^   ^
  Sa Ri  Ga Ma   Pa Dha Ni  Sa'(tara)

Octave:   .S .R (mandra/low)  |  S R (madhya/mid)  |  S' R' (tara/high)
Duration: S; = 2×  S: = ½×  S:: = ¼×
Gamakas:  ~ kampita  / jaru-up  \ jaru-down  ^ sphurita  w andola  v pratyaghata
Bars:     | beat bar  || section end  , half-beat  - rest
```

### Swarasthana Symbols (v0.1.3 corrected ratios)
| Symbol | Name | Ratio | Hz@Sa=240 |
|--------|------|-------|-----------|
| S | Shadjam | 1/1 | 240.00 |
| r (R1) | Suddha Ri | 16/15 | 256.00 |
| R (R2) | Chatusruti Ri | 9/8 | 270.00 |
| g (R3/G2) | Shatshruti Ri | 6/5 | 288.00 |
| G (G2) | Sadharana Ga | 6/5 | 288.00 |
| G+ (G3) | Antara Ga | 31/24 | 310.00 |
| m (M1) | Suddha Ma | 4/3 | 320.00 |
| M (M2) | Prati Ma | 45/32 | 337.50 |
| P | Panchamam | 3/2 | 360.00 |
| d (D1) | Suddha Dha | 8/5 | 384.00 |
| D (D2) | Chatushruti Dha | 17/10 | 408.00 |
| n (N1) | Shatshruti Dha | 9/5 | 432.00 |
| N (N2) | Kaisika Ni | 9/5 | 432.00 |
| N+ (N3) | Kakali Ni | 19/10 | 456.00 |

### Key Code Locations
- **swara.py** `SWARASTHANAS` dict — all 14 symbols with Fraction ratios
- **tala.py** `TalaEngine` class — `start()`, `stop()`, beat events
- **midi_generator.py** `MidiGenerator` class — install MIDIUtil (capital M+U)
- **tala.ts** `TalaEngine` class — `start()` / `stop()` / `runSync()` / `validateBar()`
- **raganotate_editor.html** — self-contained, open in any browser (no server)

---

## Version History

| Version | Date | What Changed |
|---------|------|-------------|
| **0.1.4** | 2026-03-12 | Web UI editor + TalaEngine TS + raga highlighting + notation playback |
| 0.1.3 | 2026-03-11 | 7 swarasthana ratio corrections (Option B from sawarsthanam.xlsx) |
| 0.1.2 | 2026-03-10 | TS parser.ts + renderer.ts + ai_encoder.py + all Python tests pass |
| 0.1.1 | 2026-03-10 | Spec refinement + lyrics-to-notation architecture |
| 0.1.0 | 2026-03-10 | Phase 1 — Core specification, Python frequency calculator |

---

## Pending Tasks (Next Session Priorities)

### High Priority
- [ ] **Test MIDI export locally**: `pip install MIDIUtil` → `python -m raganotate.midi_generator` → verify `test_output.mid`
  - Guide: `docs/midi_test.md`
- [ ] **Raga grammar CodeMirror lint**: Highlight out-of-raga swaras in the editor pane itself (not just SVG)
  - The raga validation logic exists: `getActiveRagaSwaras()` + `getRagaViolations()`

### Medium Priority
- [ ] **HuggingFace dataset** — Annotate 10+ Carnatic compositions in JSON using `ai_encoder.ast_to_dataset_record()`
  - Target: `dataset/annotated/` folder
  - Suggested pieces: Vathapi Ganapathim, Vatapi, Endaro Mahanubhavulu, Nagumomu, Sarasiruha
- [ ] **tala.ts npm build** — `npm run build` to verify TypeScript compiles (needs local Node.js)
- [ ] **Browser MIDI export** — Add "⬇ Export MIDI" button in web editor using Web MIDI API or downloadable binary

### Lower Priority
- [ ] **PyPI publish**: `pip install raganotate` — needs twine + PyPI account setup
- [ ] **npm publish**: `npm publish @jags111/raganotate` — needs npm account
- [ ] **Python test suite**: `pytest packages/python/` — all 8 modules with edge cases
- [ ] **Raga database expansion**: Currently 8 ragas; target 72 Melakarta ragas

---

## Known Issues / Gotchas

| Issue | Status | Fix |
|-------|--------|-----|
| `.gitattributes` lost on session reset | Fixed 2026-03-12 | File is now in repo |
| `pip install midiutil` (lowercase) → wrong package | Fixed 2026-03-12 | Use `MIDIUtil` capital |
| `swara.py` ratios can revert if file re-uploaded to GitHub | Watch | Always verify with `python -c "from raganotate.swara import SWARASTHANAS; print(SWARASTHANAS['r'].ratio)"` → should print `16/15` |
| LF/CRLF warning in GitHub Desktop | Fixed | `.gitattributes` has `* text=auto` |
| `index.lock` blocking git | If occurs | Delete `C:\Users\sunde\AI_dance\RagaNotate\.git\index.lock` manually |

---

## Quick Verification Commands

```python
# Verify swara ratios are correct
from raganotate.swara import SWARASTHANAS
for sym, sw in list(SWARASTHANAS.items()):
    print(f"  {sym}: {sw.ratio} = {float(sw.ratio)*240:.2f} Hz")
```

```python
# Verify MIDI can generate
from raganotate import parse_notation
from raganotate.midi_generator import ast_to_midi
ast = parse_notation("| S R G M | P D N S' ||", tala="Adi")
ast_to_midi(ast, "/tmp/test.mid")
print("MIDI OK")
```

```bash
# Check all versions match
grep -h "version" packages/python/raganotate/__init__.py packages/python/setup.py packages/js/package.json
```

---

## GitHub Workflow

1. Work is auto-saved to `C:\Users\sunde\AI_dance\RagaNotate\` (mounted folder)
2. At session end: run `bash checkpoint.sh "what-was-done"` → creates local bundle backup
3. Then: open GitHub Desktop → commit with message → Push to `github.com/jags111/RagaNotate`
4. If git push blocked from sandbox: use GitHub Desktop (always works)

---

*This file is updated automatically at each development checkpoint.*
*RagaNotate · github.com/jags111/RagaNotate*
