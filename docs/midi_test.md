# MIDI Export — Local Test Guide

**Package:** `raganotate` v0.1.4
**File:** `packages/python/raganotate/midi_generator.py`

---

## 1. Install MIDIUtil

```bash
pip install MIDIUtil
```

> ⚠️ The PyPI package name is **`MIDIUtil`** (capital M and U).
> `pip install midiutil` (lowercase) is a **different, older package** — do not use it.

Verify installation:
```bash
python -c "from midiutil import MIDIFile; print('MIDIUtil OK')"
```

---

## 2. Quick test — demo MIDI file

From the repo root:

```bash
cd packages/python
python -m raganotate.midi_generator
```

Expected output:
```
MIDI written to: test_output.mid
```

A `test_output.mid` file will be created in the current directory.
Open it in any DAW (GarageBand, Ableton, Logic, MuseScore, LMMS) or MIDI player to hear **Sa Re Ga Ma Pa Da Ni Sa'** ascending and descending scale in Adi Tala at 72 BPM.

---

## 3. Python API usage

```python
from raganotate import parse_notation
from raganotate.midi_generator import MidiGenerator, ast_to_midi

# Parse a notation string
ast = parse_notation("| S R G M | P D N S' | N D P M | G R S ||", tala="Adi")

# Option A: one-liner
path = ast_to_midi(ast, "vathapi.mid", sa_hz=240.0, bpm=72.0)
print(f"Written: {path}")

# Option B: fine-grained control
gen = MidiGenerator(sa_hz=240.0, bpm=90.0, program=40)  # program 40 = Violin
gen.generate(ast, "vathapi_violin.mid")
```

### MIDI program numbers (instruments)
| Number | Instrument |
|--------|-----------|
| 25     | Acoustic Guitar (nylon) — default |
| 40     | Violin |
| 42     | Cello |
| 73     | Flute |
| 75     | Pan Flute |
| 105    | Sitar |
| 108    | Kalimba |

---

## 4. Gamaka pitch bends

The MIDI generator encodes gamakas as **pitch bend sequences**:

| Gamaka | ASCII | What happens in MIDI |
|--------|-------|----------------------|
| Kampita `~` | `G~` | Oscillating pitch bend (16 steps, sine-like) |
| Jaru ascending `/` | `S/R` | Linear pitch bend up from ~95% of target |
| Jaru descending `\` | `N\D` | Linear pitch bend down from ~105% of target |
| Sphurita `^` | `M^` | Grace-up bend at note onset |
| Pratyaghata `v` | `G+v` | Grace-down bend at onset |

Pitch bend range is ±2 semitones (can be changed via `MidiGenerator.PITCH_BEND_SEMITONES`).

Example with gamakas:
```python
ast = parse_notation("| S R~ G/M | P D^ N\\S' ||", tala="Adi")
ast_to_midi(ast, "with_gamakas.mid", sa_hz=240.0, bpm=60.0)
```

---

## 5. Just Intonation tuning

All notes use **Just Intonation** frequencies (v0.1.3 corrected ratios):

| Note | Ratio | Hz (Sa=240) |
|------|-------|------------|
| Sa (S) | 1/1 | 240.00 |
| Ri1 (r) | 16/15 | 256.00 |
| Ri2 (R) | 9/8 | 270.00 |
| Ga3 (G+) | 31/24 | 310.00 |
| Ma1 (m) | 4/3 | 320.00 |
| Pa (P) | 3/2 | 360.00 |
| Dha2 (D) | 17/10 | 408.00 |
| Ni3 (N+) | 19/10 | 456.00 |

MIDI uses equal temperament, so pitch bend events compensate for JI deviation.

---

## 6. Troubleshooting

**`ModuleNotFoundError: No module named 'midiutil'`**
→ You installed `midiutil` (lowercase). Uninstall it and install `MIDIUtil`:
```bash
pip uninstall midiutil
pip install MIDIUtil
```

**`ImportError` about raganotate**
→ Install in editable mode from repo root:
```bash
cd packages/python
pip install -e .
```

**Pitch bends not working in my DAW**
→ Ensure the MIDI channel's pitch bend range is set to ±2 semitones.
In most DAWs, add a "Pitch Bend Range" MIDI effect set to 2 semitones.

**Output sounds out of tune vs Western tuning**
→ That's correct — Carnatic music uses Just Intonation, not equal temperament.
The pitch deviations are intentional and correspond to classical Carnatic tuning.

---

*RagaNotate v0.1.4 · github.com/jags111/RagaNotate*
