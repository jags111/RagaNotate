/**
 * audio.ts — Web Audio API Synthesis Engine
 * ==========================================
 * Synthesizes Carnatic swaras with gamaka pitch contours
 * using the browser's Web Audio API.
 *
 * Usage:
 *   const engine = new AudioEngine({ saHz: 240, bpm: 72 });
 *   await engine.playAST(ast);
 *
 * github.com/jags111/RagaNotate
 */

import type { NotationAST, SwaraNode, AudioOptions } from "./types";
import { GAMAKAS, applyGamakaToOscillator, GAMAKA_SYMBOL_MAP } from "./gamaka";
import { getTala, generateBeats } from "./tala";

// ---------------------------------------------------------------------------
// Swara frequency table (Just Intonation, relative to Sa = 1.0)
// ---------------------------------------------------------------------------
const SWARA_RATIOS: Record<string, number> = {
  "S":  1 / 1,
  "r":  256 / 243,
  "R":  9 / 8,
  "g":  32 / 27,
  "G":  6 / 5,
  "G+": 5 / 4,
  "m":  4 / 3,
  "M":  45 / 32,
  "P":  3 / 2,
  "d":  128 / 81,
  "D":  5 / 3,
  "n":  16 / 9,
  "N":  9 / 5,
  "N+": 15 / 8,
};

const OCTAVE_MULT: Record<string, number> = {
  mandra: 0.5,
  madhya: 1.0,
  tara:   2.0,
};

export function swaraToHz(
  symbol: string,
  octave: "mandra" | "madhya" | "tara",
  saHz: number,
): number {
  const ratio = SWARA_RATIOS[symbol] ?? 1.0;
  return ratio * saHz * OCTAVE_MULT[octave];
}

// ---------------------------------------------------------------------------
// AudioEngine
// ---------------------------------------------------------------------------
export class AudioEngine {
  private ctx: AudioContext | null = null;
  private masterGain: GainNode | null = null;

  constructor(private options: AudioOptions) {}

  private getContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.value = 0.7;
      this.masterGain.connect(this.ctx.destination);
    }
    return this.ctx;
  }

  /** Play a single swara note with optional gamaka. */
  playSwara(
    node: SwaraNode,
    startTime: number,
    durationS: number,
  ): void {
    const ctx = this.getContext();
    const targetHz = swaraToHz(node.symbol, node.octave, this.options.saHz);

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = (this.options.instrument as OscillatorType) ?? "sine";
    osc.frequency.value = targetHz;

    // Amplitude envelope (soft attack + release)
    gain.gain.setValueAtTime(0, startTime);
    gain.gain.linearRampToValueAtTime(0.8, startTime + 0.02);
    gain.gain.setValueAtTime(0.8, startTime + durationS - 0.05);
    gain.gain.linearRampToValueAtTime(0, startTime + durationS);

    osc.connect(gain);
    gain.connect(this.masterGain!);

    // Apply gamaka if present
    if (node.gamaka && node.gamaka.token !== "GMK_AHAT") {
      const onsetHz = targetHz * (
        node.gamaka.curveType === "linear_up"   ? 0.94 :
        node.gamaka.curveType === "linear_down" ? 1.06 : 1.0
      );
      applyGamakaToOscillator(osc, node.gamaka, onsetHz, targetHz, startTime, durationS);
    }

    osc.start(startTime);
    osc.stop(startTime + durationS);
  }

  /** Play an entire NotationAST. */
  async playAST(ast: NotationAST): Promise<void> {
    const ctx = this.getContext();
    await ctx.resume();

    const bpm = this.options.bpm;
    const aksharaDur = 60.0 / bpm;  // seconds per akshara
    const now = ctx.currentTime + 0.1;

    let time = now;

    for (const node of ast.nodes) {
      if (node.type === "bar" || node.type === "half_beat" || node.type === "tala") {
        continue;
      }

      if (node.type === "rest") {
        time += node.duration * aksharaDur;
        continue;
      }

      if (node.type === "swara") {
        const durationS = node.duration * aksharaDur;
        this.playSwara(node, time, durationS);
        time += durationS;
      }
    }
  }

  /** Stop all audio immediately. */
  stop(): void {
    if (this.ctx) {
      this.ctx.close();
      this.ctx = null;
      this.masterGain = null;
    }
  }

  /** Play a single test note. */
  async testTone(saHz = 240, durationS = 1.0): Promise<void> {
    const ctx = this.getContext();
    await ctx.resume();

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = saHz;
    gain.gain.setValueAtTime(0, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.5, ctx.currentTime + 0.05);
    gain.gain.linearRampToValueAtTime(0, ctx.currentTime + durationS);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + durationS);
  }
}
