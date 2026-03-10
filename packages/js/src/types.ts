/**
 * types.ts — Shared TypeScript Interfaces & Types
 * ================================================
 * All core type definitions for the RagaNotate JS/TS library.
 *
 * github.com/jags111/RagaNotate
 */

// ---------------------------------------------------------------------------
// Octave
// ---------------------------------------------------------------------------
export type Octave = "mandra" | "madhya" | "tara";

// ---------------------------------------------------------------------------
// Gamaka
// ---------------------------------------------------------------------------
export type PitchCurveType =
  | "flat"
  | "linear_up"
  | "linear_down"
  | "oscillate"
  | "wide_oscillate"
  | "grace_up"
  | "grace_down"
  | "accent"
  | "fade"
  | "complex";

export interface GamakaDefinition {
  token: string;          // e.g. "GMK_KAMP"
  symbol: string;         // ASCII notation: "~", "/", "\\"
  name: string;
  curveType: PitchCurveType;
  defaultIntensity: number;
  defaultRate: number;    // Hz for oscillation gamakas
}

// ---------------------------------------------------------------------------
// Swarasthana
// ---------------------------------------------------------------------------
export interface Swarasthana {
  number: number;
  symbol: string;         // e.g. "S", "R", "G+", "N+"
  variant: number;        // 0/1/2/3
  name: string;
  phonetic: string;       // "Sa", "Ri", "Gi"
  token: string;          // "SA_0", "RI_2"
  ratioNum: number;       // Numerator of JI ratio
  ratioDen: number;       // Denominator of JI ratio
  swaraType: "achala" | "chala";
}

export function ratioToFloat(sw: Swarasthana): number {
  return sw.ratioNum / sw.ratioDen;
}

// ---------------------------------------------------------------------------
// AST Node Types
// ---------------------------------------------------------------------------
export type NodeType =
  | "swara"
  | "rest"
  | "bar"
  | "half_beat"
  | "tala"
  | "lyrics";

export interface BaseNode {
  type: NodeType;
  raw?: string;
}

export interface SwaraNode extends BaseNode {
  type: "swara";
  symbol: string;         // Canonical: "S", "R", "G+", "N+"
  octave: Octave;
  variant: number;        // 0=default, 1/2/3
  duration: number;       // Aksharas
  gamaka?: GamakaDefinition;
  lyric?: string;
}

export interface RestNode extends BaseNode {
  type: "rest";
  duration: number;
  lyric?: string;
}

export interface BarNode extends BaseNode {
  type: "bar";
  isSectionEnd: boolean;  // true for "||"
}

export interface HalfBeatNode extends BaseNode {
  type: "half_beat";
}

export interface TalaNode extends BaseNode {
  type: "tala";
  name: string;
  jaati: string;
  speed: "prathama" | "madhyama" | "durita";
}

export interface LyricsNode extends BaseNode {
  type: "lyrics";
  syllables: string[];
}

export type ASTNode =
  | SwaraNode
  | RestNode
  | BarNode
  | HalfBeatNode
  | TalaNode
  | LyricsNode;

// ---------------------------------------------------------------------------
// Full AST Document
// ---------------------------------------------------------------------------
export interface NotationAST {
  tala?: TalaNode;
  nodes: ASTNode[];
  metadata: Record<string, string>;
}

// ---------------------------------------------------------------------------
// Tala
// ---------------------------------------------------------------------------
export type AngaType = "U" | "O" | "l" | "8" | ")" | "+";

export interface Anga {
  type: AngaType;
  jaati: number;        // 3/4/5/7/9 for Laghu
  aksharas: number;
}

export interface TalaDefinition {
  name: string;
  angas: Anga[];
  totalAksharas: number;
  description: string;
}

// ---------------------------------------------------------------------------
// Raga
// ---------------------------------------------------------------------------
export interface RagaDefinition {
  name: string;
  arohana: string[];
  avarohana: string[];
  vadi: string;
  samvadi: string;
  gamakaRules: Record<string, string[]>;   // swara → preferred GMK tokens
  description: string;
}

// ---------------------------------------------------------------------------
// Renderer options
// ---------------------------------------------------------------------------
export interface RenderOptions {
  width?: number;
  cellWidth?: number;
  cellHeight?: number;
  fontSize?: number;
  showLyrics?: boolean;
  showTalaGrid?: boolean;
  theme?: "light" | "dark";
}

// ---------------------------------------------------------------------------
// Audio options
// ---------------------------------------------------------------------------
export interface AudioOptions {
  saHz: number;
  bpm: number;
  gainDb?: number;
  reverbMix?: number;
  instrument?: "sine" | "sawtooth" | "triangle" | "custom";
}
