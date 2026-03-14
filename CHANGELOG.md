# Changelog

All notable changes to **RagaNotate** will be documented in this file.

This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.2.0] — 2026-03-14

### Added — Canonical Notation Standard + 72 Melakarta DB + Geetham Editor

#### Notation Standard (PCM / Raga Sangrah)
- **Three-system notation support** — ASCII keyboard input, Unicode dot-above/below display, subscript variants
  - Tara sthayi: `S'` (ASCII) = `Ṡ` U+1E60 = dot-above
  - Mandra sthayi: `.S` (ASCII) = `Ṣ` U+1E62 = dot-below
  - Variant subscripts: R₁ R₂ R₃ / G₂ G₃ / M₁ M₂ / D₁ D₂ / N₂ N₃
- **`normalizeUnicode()`** — converts Unicode input (Ṡ, R₁ etc.) to ASCII for parsing
- **Geetham notation format** documented — based on Jayakaru Geetam (Dhanyasi, Chaturashra Dhruvam)

#### Raga Database
- 30+ ragas in editor dropdown: popular Janya + Melakarta M1 + M2 groups
- Full 72 Melakarta raga reference in `References/RAGA_DATABASE.md`
- ~45 key Janya ragas with parent melakarta, Vadi, Samvadi
- Aliases: `'Kalyani'` → Mechakalyani, `'Pantuvarali'` → Kamavardhini

#### `web/raganotate_editor.html` — v0.2.0

**Three-tab layout:**
- **Notation Editor** (CodeMirror live editor + SVG preview)
- **Geetham / Composition Editor** ← new
- **Raga Reference** — searchable table ← new

**Geetham Editor (new):**
- Composition header: title, raga, tala, arohanam, avarohanam, composer
- Section blocks: Pallavi, Anupallavi, Charanam (add/remove)
- Per-bar notation + lyrics aligned cell rows
- Real-time SVG preview per section
- Pre-loaded with Jayakaru Geetam Pallavi
- ▶ Play Geetham + ⬇ Export SVG

**Enhanced controls:**
- Sa frequency: full chromatic (C 240 Hz traditional → all 12 notes → A3 220 Hz)
- BPM presets: Vilamba 60 / Madhya 80 / Durita 120 / Fast 160 / V.Fast 200
- Chapu talas: Thisra (3), Khanda (5), Misra (7)
- Gamaka playback: kampita, jaru_up/down, sphurita, andola all synthesized
- Nokku gamaka (`*`) added

**Display:**
- SVG shows Unicode: `Ṡ` for tara, `R₂` / `G₃` for variants
- Tara/mandra notes distinct colours in CodeMirror
- Floating notation reference panel

#### `web/swarasthana_explorer.html` — New
- Interactive 16-swarasthana reference tool (700 lines)

#### `.gitignore` improvements
- Added `init.py` / `**/init.py` (removes GitHub placeholder stubs)
- Added `*.~lock.*` (LibreOffice/Excel lock files)

### Fixed
- `__pycache__` `.pyc` files removed from git tracking
- `swara.py` docstring updated with full 72-melakarta JI context

---

## [0.1.4] — 2026-03-12

### Added — Web UI + TalaEngine TS + Shruti Drone + Audio Engine

- `web/raganotate_editor.html` — self-contained live editor (CodeMirror + SVG + Web Audio)
- Tala Beat Clock (all 8 talas), Shruti Drone (Sa/Pa/Sa'), ▶ Play Notation
- `packages/js/src/tala.ts` — full TalaEngine TypeScript class
- `packages/python/requirements.txt` — documented with extras [midi] [audio] [ai]
- `docs/midi_test.md` — MIDI test guide
- `.gitattributes` recreated
- `CHANGELOG.md`, `SESSION_STATE.md` created

---

## [0.1.3] — 2026-03-11

### Changed — Swarasthana Ratio Corrections (Option B)

7 ratios corrected in `swara.py` against `sawarsthanam.xlsx` (ratios as ground truth):

| Symbol | Old Ratio | New Ratio | Old Hz@240 | New Hz@240 |
|--------|-----------|-----------|-----------|-----------|
| r (R1) | 256/243 | **16/15** | 252.83 | **256.00** |
| g (R3/G2) | 32/27 | **6/5** | 284.44 | **288.00** |
| G+ (G3) | 5/4 | **31/24** | 300.00 | **310.00** |
| d (D1) | 128/81 | **8/5** | 379.26 | **384.00** |
| D (D2) | 5/3 | **17/10** | 400.00 | **408.00** |
| n (N1) | 16/9 | **9/5** | 426.67 | **432.00** |
| N+ (N3) | 15/8 | **19/10** | 450.00 | **456.00** |

---

## [0.1.2] — 2026-03-10

### Added — TypeScript AST Pipeline + AI Encoder + Python Tests ✅

- `packages/js/src/parser.ts` — full AST builder
- `packages/js/src/renderer.ts` — AST → SVG
- `packages/python/raganotate/ai_encoder.py` — 2549-token vocab, 12-dim features, HuggingFace format
- All 6 Python modules tested and passing

---

## [0.1.1] — 2026-03-10

### Changed — Spec Refinement + Lyrics-to-Notation Architecture

- Gamaka symbols simplified: `/` `\` `^` `~` `w` `v`
- Numeric swara variants: G1/G2/G3
- Lyrics block format added to SPEC.md

---

## [0.1.0] — 2026-03-10

### Added — Core Specification (Phase 1)

- 3-octave ASCII notation standard
- 16 swarasthanas with JI ratios, AI tokens, phonetic encoding
- 15 gamakas with AI feature vectors
- Suladi Sapta Tala + Chapu system
- Python frequency calculator
- `web/carnatic_workflow.html` — 6-panel interactive workflow chart

---

## Version History

| Version | Date | Phase | Status |
|---------|------|-------|--------|
| **0.2.0** | 2026-03-14 | Canonical notation + 72 Melakarta DB + Geetham Editor | ✅ Complete |
| 0.1.4 | 2026-03-12 | Web UI + TalaEngine TS + Shruti Drone | ✅ Complete |
| 0.1.3 | 2026-03-11 | Swarasthana Ratio Corrections | ✅ Complete |
| 0.1.2 | 2026-03-10 | TS parser + renderer + ai_encoder + Tests | ✅ Complete |
| 0.1.1 | 2026-03-10 | Spec + Lyrics | ✅ Complete |
| 0.1.0 | 2026-03-10 | Core Specification | ✅ Complete |
| **0.3.0** | TBD | MIDI export UI + HuggingFace dataset | 🔲 Planned |
| **0.4.0** | TBD | PyPI + npm publish | 🔲 Planned |
| **1.0.0** | TBD | Full AI Release | 🔲 Planned |

---

[Unreleased]: https://github.com/jags111/RagaNotate/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jags111/RagaNotate/compare/v0.1.4...v0.2.0
[0.1.4]: https://github.com/jags111/RagaNotate/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/jags111/RagaNotate/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/jags111/RagaNotate/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/jags111/RagaNotate/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jags111/RagaNotate/releases/tag/v0.1.0
