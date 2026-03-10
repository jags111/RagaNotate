/**
 * gamaka.ts — Gamaka Definitions & Pitch Contour Functions
 * =========================================================
 * All 15 classical Carnatic gamakas with:
 *   - ASCII notation symbols
 *   - Pitch contour functions for Web Audio API synthesis
 *
 * github.com/jags111/RagaNotate
 */

import type { GamakaDefinition, PitchCurveType } from "./types";

// ---------------------------------------------------------------------------
// Gamaka Registry
// ---------------------------------------------------------------------------
export const GAMAKAS: Record<string, GamakaDefinition> = {
  GMK_KAMP: { token: "GMK_KAMP", symbol: "~",    name: "Kampita",     curveType: "oscillate",       defaultIntensity: 0.6, defaultRate: 6.0 },
  GMK_ANDO: { token: "GMK_ANDO", symbol: "w",    name: "Andola",      curveType: "wide_oscillate",  defaultIntensity: 0.7, defaultRate: 2.0 },
  GMK_SPHU: { token: "GMK_SPHU", symbol: "^",    name: "Sphurita",    curveType: "grace_up",        defaultIntensity: 0.5, defaultRate: 0.0 },
  GMK_PRAT: { token: "GMK_PRAT", symbol: "v",    name: "Pratyaghata", curveType: "grace_down",      defaultIntensity: 0.5, defaultRate: 0.0 },
  GMK_NOKK: { token: "GMK_NOKK", symbol: "*",    name: "Nokku",       curveType: "accent",          defaultIntensity: 0.9, defaultRate: 0.0 },
  GMK_EJRU: { token: "GMK_EJRU", symbol: "/",    name: "Etra Jaru",   curveType: "linear_up",       defaultIntensity: 0.6, defaultRate: 0.0 },
  GMK_IJRU: { token: "GMK_IJRU", symbol: "\\",   name: "Irakka Jaru", curveType: "linear_down",     defaultIntensity: 0.6, defaultRate: 0.0 },
  GMK_TRIB: { token: "GMK_TRIB", symbol: "tr",   name: "Tribhinna",   curveType: "complex",         defaultIntensity: 0.6, defaultRate: 0.0 },
  GMK_MISR: { token: "GMK_MISR", symbol: "gl",   name: "Misrita",     curveType: "complex",         defaultIntensity: 0.5, defaultRate: 0.0 },
  GMK_AHAT: { token: "GMK_AHAT", symbol: "",     name: "Ahata",       curveType: "flat",            defaultIntensity: 1.0, defaultRate: 0.0 },
  GMK_ULLA: { token: "GMK_ULLA", symbol: "vib",  name: "Ullasita",    curveType: "oscillate",       defaultIntensity: 0.7, defaultRate: 8.0 },
};

// Symbol → token lookup (including aliases)
export const GAMAKA_SYMBOL_MAP: Record<string, string> = {
  "~":    "GMK_KAMP",
  "~~":   "GMK_KAMP",
  "w":    "GMK_ANDO",
  "nd":   "GMK_ANDO",
  "^":    "GMK_SPHU",
  "sp":   "GMK_SPHU",
  "v":    "GMK_PRAT",
  "*":    "GMK_NOKK",
  "/":    "GMK_EJRU",
  "\\":   "GMK_IJRU",
  "tr":   "GMK_TRIB",
  "gl":   "GMK_MISR",
  "vib":  "GMK_ULLA",
};

export function parseGamakaSymbol(sym: string): GamakaDefinition {
  const token = GAMAKA_SYMBOL_MAP[sym];
  return token ? GAMAKAS[token] : GAMAKAS["GMK_AHAT"];
}

// ---------------------------------------------------------------------------
// Pitch Contour Functions
// ---------------------------------------------------------------------------

/** Returns a pitch function f(t) → Hz for gamaka animation. */
export function getPitchContour(
  gamaka: GamakaDefinition,
  onsetHz: number,
  targetHz: number,
  durationS: number,
): (t: number) => number {
  const { curveType, defaultRate, defaultIntensity } = gamaka;
  const amp = targetHz * 0.02;

  switch (curveType) {
    case "flat":
      return () => targetHz;

    case "linear_up":
      return (t) => onsetHz + (targetHz - onsetHz) * (t / Math.max(durationS, 1e-6));

    case "linear_down":
      return (t) => onsetHz - (onsetHz - targetHz) * (t / Math.max(durationS, 1e-6));

    case "oscillate":
      return (t) => targetHz + amp * Math.sin(2 * Math.PI * defaultRate * t);

    case "wide_oscillate":
      return (t) => targetHz + (targetHz * 0.04) * Math.sin(2 * Math.PI * 2.0 * t);

    case "grace_up": {
      const eps = targetHz * 0.05;
      const trans = durationS * 0.2;
      return (t) => t < trans ? targetHz + eps * (1 - t / trans) : targetHz;
    }

    case "grace_down": {
      const eps = targetHz * 0.05;
      const trans = durationS * 0.2;
      return (t) => t < trans ? targetHz - eps * (1 - t / trans) : targetHz;
    }

    case "accent": {
      const spike = targetHz * 0.01;
      const attack = durationS * 0.1;
      return (t) => t < attack
        ? targetHz + spike * Math.sin(Math.PI * t / attack)
        : targetHz;
    }

    case "fade":
      return () => targetHz;

    default:
      return () => targetHz;
  }
}

// ---------------------------------------------------------------------------
// Web Audio API — apply gamaka to OscillatorNode
// ---------------------------------------------------------------------------

/**
 * Apply a gamaka contour to a Web Audio OscillatorNode frequency parameter.
 *
 * @param osc        Web Audio OscillatorNode (already connected)
 * @param gamaka     GamakaDefinition
 * @param onsetHz    Starting frequency
 * @param targetHz   Target frequency
 * @param startTime  AudioContext time to start
 * @param duration   Duration in seconds
 */
export function applyGamakaToOscillator(
  osc: OscillatorNode,
  gamaka: GamakaDefinition,
  onsetHz: number,
  targetHz: number,
  startTime: number,
  duration: number,
): void {
  const freq = osc.frequency;
  const steps = 32;
  const stepDur = duration / steps;
  const pitchFn = getPitchContour(gamaka, onsetHz, targetHz, duration);

  freq.cancelScheduledValues(startTime);
  freq.setValueAtTime(pitchFn(0), startTime);

  for (let i = 1; i <= steps; i++) {
    const t = i * stepDur;
    freq.linearRampToValueAtTime(pitchFn(t), startTime + t);
  }
}
