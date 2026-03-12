# Changelog

All notable changes to **RagaNotate** will be documented in this file.

This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.1.4] — 2026-03-12

### Added — Web UI Editor + Tala Clock + Shruti Drone

#### `web/raganotate_editor.html` — Self-contained Live Editor
- **CodeMirror 5** editor with custom `raganotate` syntax mode
  - Colour tokens: achala swaras (amber), chala swaras (blue), gamaka (teal), bars (accent), rest (muted), meta (purple)
  - Toolbar quick-insert buttons: `|` `||` `-` `,` `~` `/` `\` `^` `w` `;` `:` `'` `.`
- **Real-time SVG preview** — live re-renders on every keystroke (300ms debounce)
  - Swara boxes with octave dots (tara above, mandra below)
  - Gamaka indicators (top-right corner)
  - Duration width-stretching (double for `;`, half for `:`)
  - Bar lines, section-end double bars, half-beat markers
  - Auto row-wrap at viewport width
  - Dark / light theme toggle
- **Tala Beat Clock** — visual anga display for all 8 talas
  - Anga groups coloured: Laghu (blue), Drutam (green), Anudruta (purple)
  - Current beat highlighted with pulse animation
  - Beat counter display (1/8, 3/8 etc)
- **Audio Engine** (Web Audio API — no server needed)
  - 🥁 **Mridangam**: Thom (bass sine + pitch-drop), Ta/Dhi (noise bandpass), Ki (crisp high click)
    - Sam = Thom + strong Ta; Laghu start = strong Ta; Drutam wave = Ki
  - 🎹 **Harmonium**: Sawtooth + harmonics through low-pass filter, tuned to Sa intervals
  - 🔔 **Bell / Gong**: Metallic partials at real bell frequency ratios (2.756×, 5.404×, 8.933×)
  - ◻ **Silent** mode
- **Shruti Drone** — Sa, Pa, Sa' toggle buttons
  - 4 detuned sawtooth oscillators (chorus effect) + fundamental sine
  - Low-pass filtered for warmth; 1.5s fade-in
  - Animated waveform visualiser bars
- Controls: Raga selector (8 ragas), Sa Hz (C, C#, D … 11 options), Tala selector, BPM slider 40–240
- SVG export button (downloads `raganotate_notation.svg`)

#### `requirements.txt` — Fully documented dependency list
- Added `MIDIUtil>=1.2.1` with PyPI capitalisation note (NOT `midiutil`)
- Added `soundfile>=0.12.1`, `svgwrite>=1.4.3`
- Added `datasets>=2.14.0`, `tokenizers>=0.15.0`, `transformers>=4.35.0` (AI extras)
- Added install notes for Windows, real-time audio (`pyaudio`, `simpleaudio`)
- Documented install extras: `[midi]`, `[audio]`, `[ai]`, `[all]`

### Planned
- Web UI live editor (HTML + CodeMirror + real-time SVG preview)
- Tala beat clock visual component
- Raga grammar live validator
- MIDI export UI (browser download)
- HuggingFace dataset publication
- PyPI package: `pip install raganotate`
- npm package: `@jags111/raganotate`

---

## [0.1.2] — 2026-03-10

### Added — TypeScript AST Pipeline + AI Encoder + Full Python Tests

#### TypeScript — `packages/js/src/`

**`parser.ts`** — Full AST builder wired to lexer
- `parseNotation(str, tala, jaati, speed) → NotationAST`
- Handles all token kinds: SWARA, BAR, SECTION_END, REST, HALF_BEAT, TALA_HEADER
- Swara token parser: octave prefix (`.`), tara suffix (`'`), gamaka suffix, duration (`;`/`:`), variant digit (`1/2/3`)
- Full `VARIANT_ALIAS` table: G1/G2/G3 → g/G/G+ etc.
- Helper functions: `getSwaras()`, `getBars()`, `totalDuration()`, `annotateWithLyrics()`

**`renderer.ts`** — AST → SVG visual notation
- Swara boxes with symbol text, octave dots (tara above / mandra below)
- Gamaka indicator (top-right corner, teal coloured)
- Duration width-stretching (double cells for `S;`, half cells for `S:`)
- Bar lines (single `|` and double `||` section end)
- Half-beat comma markers
- Optional lyric text below each swara
- Optional tala grid background stripe
- Row auto-wrap at configurable width
- **Light and dark themes** with full palette
- `renderHTML(ast, opts)` convenience wrapper for full HTML page output
- Inspired by: [srikumarks/carnot](https://github.com/srikumarks/carnot)

#### Python — `raganotate/`

**`ai_encoder.py`** — Notation → AI token sequences
- `ast_to_token_sequence(ast)` → flat `list[str]` for LLM tokenization
  - Token format: `[MD]RI_2:GMK_KAMP`, `[HI]SA_0:GMK_AHAT`
  - Special tokens: `[BOS]`, `[EOS]`, `[BAR]`, `[SBAR]`, `[REST]`, `[TALA:Adi]`, `[LYR:syllable]`
- `ast_to_feature_matrix(ast)` → `list[SwaraFeature]` (12-dim vectors)
  - Dims: hz, ratio_num, ratio_den, octave_id, swara_id, duration, gamaka_id, curve_type, intensity, rate, bar_position, tala_aksharas
- `ast_to_dataset_record(ast)` → HuggingFace-compatible JSON dict
- `ast_to_phonetic(ast)` → `"Sa Ri Gi Pa | Ni Sa' ..."` readable string
- `build_vocabulary()` → full 2,549-token vocabulary for tokenizer training

#### Python — Tests Validated ✅
All 6 modules tested and passing:

| Module | Test Result |
|--------|------------|
| `swara.py` | ✅ 16 swarasthanas, all Hz correct, G3→G+ resolved |
| `gamaka.py` | ✅ 15 gamakas, feature vectors, pitch contour samples |
| `tala.py` | ✅ All 8 talas, beat clock @ 80 BPM, 8 beat events |
| `parser.py` | ✅ `| S R~ G M | P/D N S' |` → 20 nodes, 15 swaras, correct gamakas |
| `lyrics_mapper.py` | ✅ "Va-tha-pi Ga-na-pa-tim" → 9 syllables, aligned to swaras |
| `ai_encoder.py` | ✅ 27 tokens, 12-dim features, phonetic string, 2549-token vocab |

#### Bug Fixes
- Fixed f-string backslash syntax error in `swara.py` (Python <3.12 compatibility)
- Removed undefined `GamakaType` reference from `__init__.py`
- Made `midi_generator` import lazy (not imported at package level) to avoid crash when `midiutil` unavailable

### Updated Files
- `packages/js/src/parser.ts` ← **New**
- `packages/js/src/renderer.ts` ← **New**
- `packages/python/raganotate/ai_encoder.py` ← **New**
- `packages/python/raganotate/swara.py` — f-string backslash fix
- `packages/python/raganotate/__init__.py` — removed GamakaType, lazy midi import

### Planned
- Tala beat pattern generator (`tala.ts`)
- Python `raganotate` package (swara, gamaka, tala, parser, renderer, ai_encoder)
- MIDI export from Python parser
- AI tokenizer for LLM training
- Web UI live editor (HTML + CodeMirror + real-time SVG)
- Gamaka pitch contour visualizer
- Tala beat clock UI
- Raga grammar validator
- Annotated compositions dataset (50+ pieces, JSON/CSV)
- HuggingFace dataset publication
- PyPI package: `pip install raganotate`
- npm package: `@jags111/raganotate`

---

## [0.1.1] — 2026-03-10

### Changed — Spec Refinement & Lyrics-to-Notation Architecture

#### Notation Symbols Revised
- Simplified gamaka symbol set for human-readability and code parsing:
  - `/` = Jaru ascending (was `~/`), e.g. `S/R G/M`
  - `\` = Jaru descending (was `v`), e.g. `S\N G\R`
  - `^` = Sphurita grace-up, e.g. `M1^ P D^`
  - `~` = Kampita (oscillation), e.g. `G3~ M1 P`
  - `w` = Andola (slow wide oscillation), e.g. `G2w D1w`
  - `v` = Pratyaghata grace-down (retained)
  - Added: `tr` (Tribhinna), `gl` (generic glide), `sp` (sphurita alias), `nd` (andola alias), `vib` (vibrato)
- Added numeric swara variant suffix system: `G1`, `G2`, `G3` for Suddha/Sadharana/Antara Ga

#### Tala System Refined
- Matya Tala clarified: 9 aksharas (Laghu + Drutam + Laghu, Tisra jaati)
- Jhampa Tala: 10 aksharas (Misra Laghu 7 + Anudruta 1 + Drutam 2)
- Adi Tala explicitly documented as Chatusra Jati Triputa = `l4 O O` = 8 aksharas

#### Lyrics-to-Notation Mapping Added (Section 9, SPEC.md)
- Syllable-to-swara mapping rules
- Melisma notation: `(S R G)ya` — one syllable over multiple swaras
- Lyrics block format defined with `{lyrics}` / `{notation}` / `{tala}` headers

#### References Greatly Expanded
- Added 7 Carnatic AI/ML GitHub repos
- Added 5 audio/music generation repos
- Added 7 tala theory web references

### Updated Files
- `SPEC.md` → v0.1.1 (gamaka symbols, tala counts, lyrics mapping, full references)
- `todo.md` → GitHub repo URL, version tag, new references

---

## [0.1.0] — 2026-03-10

### Added — Core Specification (Phase 1 Complete)

#### Notation Standard
- Defined 3-octave ASCII notation system (Mandra / Madhya / Tara Sthayi)
- Octave markers: `.s .r .g` (mandra), `S R G` (madhya), `S' R' G'` (tara)
- Duration markers: `S` (1 akshara), `S;` (2×), `S:` (½), `S::` (¼)
- Beat markers: `|` (beat), `||` (section end), `,` (half-beat gap), `-` (rest), `_` (grace gap)

#### 16 Swarasthanas — Complete Table
- All 16 swarasthanas mapped with:
  - Short symbol (S, R, G, m, M, P, D, N, r, g, d, n, G+, N+)
  - Phonetic encoding (Sa, Ri, Gi, Ma, Mi, Pa, Di, Ni, Ra, Ga, Da, Na, Gu, Nu)
  - AI token format: `SA_0`, `RI_1`, `RI_2`, `GA_1` … `NI_3`
  - Just Intonation frequency ratios (Hz at Sa=240, Sa=256, Sa=261.63)
  - Achala / Chala classification

#### Python Frequency Calculator
- `swara_hz(symbol, octave, sa_hz)` — returns Hz for any swarasthana
- `print_scale(sa_hz)` — prints full 16-swara table for given tonic
- Octave multipliers: mandra=0.5, madhya=1.0, tara=2.0
- Based on `fractions.Fraction` for exact Just Intonation arithmetic

#### 15 Gamakas — Full AI Encoding
- All 15 classical gamakas (Natya Shastra / Sangita Sampradaya Pradarshini)
- ASCII notation symbols: `~~` `^` `v` `*` `(^)` `(v)` `{or}` `{mu}` `=` etc.
- AI token identifiers: `GMK_KAMP`, `GMK_ANDO`, `GMK_SPHU` … `GMK_ULLA`
- 6-dimensional ML feature vector per gamaka:
  `[onset_pitch, target_pitch, duration_beats, pitch_curve_type, intensity, raga_context]`
- 10 pitch curve types: flat, linear_up, linear_down, oscillate, wide_oscillate,
  grace_up, grace_down, accent, fade, complex

#### Tala System
- Suladi Sapta Talas (7 talas) with full anga structure
- 3 core angas: Anudhrutam (U/1), Dhrutam (O/2), Laghu (l/3–9)
- 5 Laghu jaatis: Tisra(3), Chatusra(4), Khanda(5), Misra(7), Sankeerna(9)
- Extended anga system: Guru(8), Plutam(12), Kakapadam(16) — 108-tala system
- 4 Chapu talas: Thisra(3), Khanda(5), Misra(7), Sankeerna(9)
- Notation example: Adi Tala = `l4 O O` = 8 aksharas

#### Repository & Tooling
- Defined full `RagaNotate/` repository directory structure
- Created `todo.md` master specification and roadmap
- Created `carnatic_workflow.html` — interactive workflow chart (6-panel)
- GitHub repository target: `github.com/jags111/RagaNotate`

### References
- [srikumarks/carnot](https://github.com/srikumarks/carnot)
- [ragasangrah.com/gamakas](https://ragasangrah.com/gamakas)
- [iSargam — Springer 2016](https://link.springer.com/article/10.1186/s13636-016-0083-z)
- *Sangita Sampradaya Pradarshini* — Subbarama Dikshitar
- *Natya Shastra* — Bharata Muni

---

## Version History Summary

| Version | Date | Phase | Status |
|---------|------|-------|--------|
| 0.1.2 | 2026-03-10 | TS parser.ts + renderer.ts + ai_encoder.py + Tests | ✅ Complete |
| 0.1.1 | 2026-03-10 | Spec Refinement + Lyrics-to-Notation Architecture | ✅ Complete |
| 0.1.0 | 2026-03-10 | Phase 1 — Core Specification | ✅ Complete |
| 0.2.0 | TBD | Phase 2 — TypeScript Library | 🔲 Planned |
| 0.3.0 | TBD | Phase 3 — Python Package | 🔲 Planned |
| 0.4.0 | TBD | Phase 4 — Web UI | 🔲 Planned |
| 0.5.0 | TBD | Phase 5 — GitHub CI/CD + Examples | 🔲 Planned |
| 1.0.0 | TBD | Phase 6 — Dataset + AI Release | 🔲 Planned |

---

[Unreleased]: https://github.com/jags111/RagaNotate/compare/v0.1.4...HEAD
[0.1.4]: https://github.com/jags111/RagaNotate/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/jags111/RagaNotate/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/jags111/RagaNotate/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/jags111/RagaNotate/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jags111/RagaNotate/releases/tag/v0.1.0
