# RagaNotate — Notation Specification

> **Version:** 0.1.1
> **Author:** Jags (jags111) · [github.com/jags111](https://github.com/jags111)
> **Repository:** [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)
> **Updated:** 2026-03-10
> **Core Integration:** [ragasangrah.com](https://ragasangrah.com/) · [srikumarks/carnot](https://github.com/srikumarks/carnot)

---

## 1. Swara Notation — Octaves

```
TARA STHAYI   (Upper Octave):  S'  R'  G'  M'  P'  D'  N'
MADHYA STHAYI (Middle Octave):  S   R   G   M   P   D   N
MANDRA STHAYI (Lower Octave):  .s  .r  .g  .m  .p  .d  .n
```

---

## 2. Duration Markers

| Symbol | Duration | Meaning |
|--------|----------|---------|
| `S`    | 1 akshara | Full beat |
| `S;`   | 2 aksharas | Double duration |
| `S:`   | 0.5 aksharas | Half beat |
| `S::` | 0.25 aksharas | Quarter beat |

---

## 3. Beat & Structure Markers

| Symbol | Meaning | Example |
|--------|---------|---------|
| `\|`   | Beat / Avartanam separator (bar line) | `S R G M \| P D N S'` |
| `\|\|` | End of section / composition | `G R S \|\|` |
| `,`    | Half-beat visible gap | `S, R G M` |
| `-`    | Rest / silence | `S R - G M` |
| `_`    | Invisible grace timing gap | `S_R G` |

---

## 4. Swara Variants — Numbering Suffix

Swaras with multiple swarasthanas use a numeric suffix for precision:

| Suffix | Meaning | Example |
|--------|---------|---------|
| No suffix | Default / context-determined | `G` = Sadharana or Antara (raga-defined) |
| `1` | Suddha / lowest variant | `G1` = Suddha Gandharam (32/27) |
| `2` | Chatusruti / middle variant | `G2` = Sadharana Gandharam (6/5) |
| `3` | Shatsruti / Antara / highest | `G3` = Antara Gandharam (5/4) |

Applied to: R (r/R), G (g/G/G+), M (m/M), D (d/D), N (n/N)

---

## 5. 16 Swarasthanas (Just Intonation)

> **Sa is relative.** All frequencies are ratios of the performer's Adhara Shadjam.
> Common values: **240 Hz** (traditional) · **256 Hz** (scientific) · **261.63 Hz** (C4) · **220 Hz** (lower male voice)

| # | Symbol | Variant | Phonetic | AI Token | Ratio | Hz@240 | Hz@261.63 | Type |
|---|--------|---------|----------|----------|-------|--------|-----------|------|
| 1  | S   | —  | Sa  | SA_0     | 1/1     | 240.00 | 261.63 | Achala |
| 2  | r / R1 | Suddha | Ra | RI_1  | 256/243 | 252.84 | 275.62 | Chala |
| 3  | R / R2 | Chatusruti | Ri | RI_2 | 9/8   | 270.00 | 294.33 | Chala |
| 4  | g / G1 | Suddha/Shatsruti Ri | Ga | GA_1 | 32/27 | 284.44 | 309.87 | Chala |
| 5  | G / G2 | Sadharana | Gi | GA_2 | 6/5  | 288.00 | 313.96 | Chala |
| 6  | G+ / G3 | Antara | Gu | GA_3 | 5/4  | 300.00 | 327.04 | Chala |
| 7  | m / M1 | Suddha | Ma | MA_1 | 4/3  | 320.00 | 348.83 | Chala |
| 8  | M / M2 | Prati  | Mi | MA_2 | 45/32 | 337.50 | 367.92 | Chala |
| 9  | P   | —  | Pa  | PA_0     | 3/2     | 360.00 | 392.44 | Achala |
| 10 | d / D1 | Suddha | Da | DA_1 | 128/81 | 379.26 | 413.43 | Chala |
| 11 | D / D2 | Chatusruti | Di | DA_2 | 5/3  | 400.00 | 436.05 | Chala |
| 12 | n / N1 | Suddha/Shatsruti Dha | Na | NI_1 | 16/9 | 426.67 | 465.11 | Chala |
| 13 | N / N2 | Kaisika | Ni | NI_2 | 9/5  | 432.00 | 470.93 | Chala |
| 14 | N+ / N3 | Kakali | Nu | NI_3 | 15/8 | 450.00 | 490.55 | Chala |
| 15 | S'  | Upper | Sa' | SA_0_HI | 2/1  | 480.00 | 523.25 | Achala |
| 16 | .s  | Lower | .sa | SA_0_LO | 1/2  | 120.00 | 130.81 | Achala |

**Shared pitches:** G1 = R3 (Shatsruti Ri) · N1 = D3 (Shatsruti Dha) — same frequency, different name by raga context.

**Typical usage (simplified 8-swara set, Sa = 240 Hz):**

| Swara | Ratio | Hz | Notes |
|-------|-------|----|-------|
| Sa    | 1/1   | 240 | Tonic |
| Ri    | 9/8   | 270 | Chatusruti Ri |
| Ga    | 6/5 or 5/4 | 288 or 300 | Sadharana or Antara |
| Ma    | 4/3 or 17/12 | 320 | Suddha or Prati |
| Pa    | 3/2   | 360 | Panchama |
| Dha   | 27/16 or 5/3 | 405 | Chatusruti or Suddha |
| Ni    | 15/8  | 450 | Kakali |
| Sa'   | 2/1   | 480 | Upper octave |

---

## 6. AI Phonetic Vowel Encoding

```
Suffix 'a'  →  Suddha / lower variant:       Ra (Suddha Ri),  Da (Suddha Dha)
Suffix 'i'  →  Chatusruti / middle variant:   Ri (Chatusruti Ri), Di (Chatusruti Dha)
Suffix 'u'  →  Kakali / Shatsruti / upper:    Gu (Antara Ga), Nu (Kakali Ni)

AI Token full format:  {OCTAVE_PREFIX}_{SWARA}_{VARIANT}
  LO_ = Mandra Sthayi · MD_ = Madhya Sthayi · HI_ = Tara Sthayi
  Example:  HI_RI_2  =  Chatusruti Rishabham in Tara Sthayi
```

---

## 7. Gamaka Notation Symbols

Gamakas are ornamental phrases applied to a swara. The symbol follows the swara it modifies.

### Primary Gamaka Set

| Symbol | Name | Type | Description | Example |
|--------|------|------|-------------|---------|
| *(none)* | Ahata | Direct | Plain note, no ornament | `S R G M` |
| `~`  | Kampita | Oscillation | Vibrato-like oscillation between adjacent svaras | `G3~ M1 P` |
| `/`  | Jaru (ascending) | Slide up | Upward glide/portamento to target | `S/R G/M` |
| `\`  | Jaru (descending) | Slide down | Downward glide/portamento to target | `S\N G\R` |
| `^`  | Sphurita | Grace-up | Touch note above, land on target | `M1^ P D^` |
| `v`  | Pratyaghata | Grace-down | Touch note below, land on target | `P v M G` |
| `w`  | Andola | Wide oscillation | Slow wide oscillation; pitch meanders without landing | `G2w D1w` |
| `tr` | Tribhinna | Complex | Three-string / three-pitch ornament | `Ptr G` |
| `gl` | Gamaka-glide | Slide | Generic portamento (combined up+down) | `Sgl R` |
| `sp` | Sphurita (explicit) | Grace-up | Alias for `^` in verbose notation | `Msp P` |
| `nd` | Andola (explicit) | Wide oscillation | Alias for `w` in verbose notation | `Gnd D` |
| `vib`| Vibrato | Oscillation | Sustained kampita, wider range | `Nvib S'` |

### Full Descriptive Block
For precise AI encoding, use braces:
```
{gmk:kamp,onset:G3,target:M1,dur:0.5,intensity:0.8}
```

### Notation Examples

```
# Plain (Ahata)
S R G M | P D N S'

# With Gamakas
S R~~ G M  →  R has kampita
S/R G/M    →  ascending jaru into R, into M
S\N G\R    →  descending jaru from S to N, G to R
M1^ P D^   →  sphurita on M1 and D
G2w D1w    →  andola on G2 and D1
```

---

## 8. Tala System

### Three Core Angas

| Anga | Symbol | Aksharas | Hand Action |
|------|--------|----------|-------------|
| Anudhrutam | `U` | 1 | Downward palm clap |
| Dhrutam    | `O` | 2 | Palm-down + palm-up |
| Laghu      | `l` | 3–9 (jaati-dependent) | Clap + finger count |

### Laghu Jaatis (Rhythmic Subdivisions)

| Jaati | Aksharas | Symbol | Solkattu |
|-------|----------|--------|----------|
| Tisra     | 3 | `l3` | Tha Ki Ta |
| Chatusra  | 4 | `l4` | Tha Ka Dhi Mi |
| Khanda    | 5 | `l5` | Tha Ka Tha Ki Ta |
| Misra     | 7 | `l7` | Tha Ki Ta Tha Ka Dhi Mi |
| Sankeerna | 9 | `l9` | Tha Ka Dhi Mi Tha Ka Tha Ki Ta |

### Suladi Sapta Talas

| Tala Name | Anga Pattern | Aksharas (Chatusra Jaati) | Notes |
|-----------|-------------|--------------------------|-------|
| **Dhruva**  | `l O l l`   | 14 | — |
| **Matya**   | `l O l`     | 9  | 3+2+4 or 4+2+4 by jaati |
| **Rupaka**  | `O l`       | 6  | Most common in bhajans |
| **Jhampa**  | `l U O`     | 10 | Misra Laghu (7+1+2) |
| **Triputa** | `l O O`     | 7  | Chatusra → **Adi Tala** (8 beats) |
| **Ata**     | `l l O O`   | 14 | — |
| **Eka**     | `l`         | 4  | Single Laghu |

> **Adi Tala** = Chatusra Jati Triputa = `l4 O O` = 4+2+2 = **8 aksharas** (most commonly used)

### Chapu Talas (Non-Anga)

| Name | Beats | Pattern | Solkattu |
|------|-------|---------|----------|
| Thisra Chapu    | 3 | 1+2 | Tha-Ki-Ta |
| Khanda Chapu    | 5 | 2+3 | Tha-Ka-Tha-Ki-Ta |
| Misra Chapu     | 7 | 3+4 | Tha-Ki-Ta-Tha-Ka-Dhi-Mi |
| Sankeerna Chapu | 9 | 4+5 | Tha-Ka-Dhi-Mi-Tha-Ka-Tha-Ki-Ta |

### Extended Anga System (108-Tala)

| Anga | Symbol | Aksharas |
|------|--------|----------|
| Anudrutam | `U` | 1  |
| Druta     | `O` | 2  |
| Laghu     | `l` | 3–9 |
| Guru      | `8` | 8  |
| Plutam    | `)` | 12 |
| Kakapadam | `+` | 16 |

---

## 9. Lyrics-to-Notation Mapping

When mapping song lyrics to swaras, each syllable maps to one swara position:

```
LYRICS:    ya   -   mu  -  na  -  ka  -
NOTATION:  S    R   G   M  P   D  N   S'
TALA:      |    Adi beat 1        |  beat 2
```

**Rules:**
- One syllable = one akshara (default)
- Long syllable (`aa`, `ee`) = two aksharas (`S;`)
- Short/unstressed syllable = half akshara (`S:`)
- Melisma (one syllable, multiple notes) = swara group in parentheses `(S R G)ya`
- Rest/held note = `-`
- Gamaka suffix placed after the swara token, before whitespace

**Lyrics block format:**
```
{lyrics}
ya  mu  na  ka  la  ya  di  pa
{notation}
S   R~  G   M   P   D   N   S'
{tala: Adi}
```

---

## 10. Full Notation Quick Reference

```
# Octaves
MANDRA:  .s  .r  .g  .m  .p  .d  .n
MADHYA:   S   R   G   M   P   D   N
TARA:    S'  R'  G'  M'  P'  D'  N'

# Duration: S (1) | S; (2) | S: (0.5) | S:: (0.25)

# Structure: | (beat) | || (section) | , (half-beat) | - (rest) | _ (grace gap)

# Gamakas: ~ (kampita)  / (jaru up)  \ (jaru down)
#           ^ (sphurita)  v (pratyaghata)  w (andola)
#           tr (tribhinna)  gl (glide)  vib (vibrato)

# Tala: Adi = l4 O O = 8 beats (most common)

# Example — Adi Tala, Madhya Sthayi with gamakas:
| S R~ G M | P/D N S' | N\ D P | M G R S ||
```

---

## 11. References

### Core Architecture
- [srikumarks/carnot](https://github.com/srikumarks/carnot) — JS SVG rendering engine for Carnatic notation
- [ragasangrah.com](https://ragasangrah.com/) — Core integration reference, gamaka examples

### Notation & Theory
- [iSargam — Springer 2016](https://link.springer.com/article/10.1186/s13636-016-0083-z) — Unicode Indian notation encoding
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

### Core Papers
- *Sangita Sampradaya Pradarshini* — Subbarama Dikshitar
- *Natya Shastra* — Bharata Muni

---

*RagaNotate SPEC v0.1.1 · 2026-03-10 · [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)*
