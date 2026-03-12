/**
 * parser.ts — Token[] → NotationAST
 * ===================================
 * Consumes tokens from lexer.ts and builds a full Abstract Syntax Tree.
 * Mirrors the structure of Python raganotate/parser.py.
 *
 * AST Node types: SwaraNode | RestNode | BarNode | HalfBeatNode | TalaNode
 *
 * github.com/jags111/RagaNotate
 */

import { tokenize, Token } from "./lexer";
import {
  NotationAST,
  SwaraNode,
  RestNode,
  BarNode,
  HalfBeatNode,
  TalaNode,
  ASTNode,
  Octave,
} from "./types";
import { parseGamakaSymbol, GAMAKA_SYMBOL_MAP } from "./gamaka";

// ---------------------------------------------------------------------------
// Swara variant alias table  (mirrors Python VARIANT_ALIAS)
// ---------------------------------------------------------------------------
const VARIANT_ALIAS: Record<string, string> = {
  R1: "r", R2: "R",
  G1: "g", G2: "G", G3: "G+",
  M1: "m", M2: "M",
  D1: "d", D2: "D",
  N1: "n", N2: "N", N3: "N+",
  // identity
  S: "S", P: "P",
};

const VALID_BASES = new Set(["S","R","G","M","P","D","N","r","g","m","d","n"]);

// ---------------------------------------------------------------------------
// Parse a single SWARA token string → SwaraNode
// ---------------------------------------------------------------------------
function parseSwaraToken(raw: string): SwaraNode | null {
  let s = raw.trim();
  let octave: Octave = "madhya";
  let variant = 0;
  let duration = 1.0;
  let gamakaSymbol: string | undefined;

  // 1. Mandra prefix
  if (s.startsWith(".")) {
    octave = "mandra";
    s = s.slice(1);
  }

  // 2. Tara suffix
  if (s.includes("'")) {
    octave = "tara";
    s = s.replace(/'/g, "");
  }

  // 3. Gamaka suffix (longest first)
  const gamakaSuffixes = [
    "~~","vib","tr","gl","sp","nd",
    "~","/","\\","^","v","w","*",
    "{or}","{ot}","{tr}","{mu}","{nm}","{mx}","{ul}",
  ];
  for (const gk of gamakaSuffixes) {
    if (s.endsWith(gk)) {
      gamakaSymbol = gk;
      s = s.slice(0, s.length - gk.length);
      break;
    }
  }

  // 4. Duration markers
  let durStr = "";
  while (s.length && (s[s.length - 1] === ";" || s[s.length - 1] === ":")) {
    durStr = s[s.length - 1] + durStr;
    s = s.slice(0, -1);
  }
  if (durStr === ";")   duration = 2.0;
  else if (durStr === ":")  duration = 0.5;
  else if (durStr === "::") duration = 0.25;

  // 5. Variant digit
  if (s.length > 1 && /[123]/.test(s[s.length - 1])) {
    variant = parseInt(s[s.length - 1], 10);
    s = s.slice(0, -1);
  } else if (s.endsWith("+")) {
    variant = 3;
    s = s.slice(0, -1);
  }

  // 6. Resolve base symbol
  const base = s.toUpperCase();
  const symKey = variant ? `${base}${variant}` : base;
  const resolved = VARIANT_ALIAS[symKey] ?? symKey;

  if (!VALID_BASES.has(s) && !VARIANT_ALIAS[symKey]) {
    return null; // unrecognised token
  }

  const gamaka = gamakaSymbol ? parseGamakaSymbol(gamakaSymbol) : undefined;

  return {
    type: "swara",
    symbol: resolved,
    octave,
    variant,
    duration,
    gamaka,
    raw,
  };
}

// ---------------------------------------------------------------------------
// Header parsers
// ---------------------------------------------------------------------------
function parseTalaHeader(tokens: Token[]): TalaNode | undefined {
  const th = tokens.find(t => t.kind === "TALA_HEADER");
  if (!th) return undefined;
  const match = /tala:\s*(\w+)/i.exec(th.value);
  if (!match) return undefined;
  return {
    type: "tala",
    name: match[1],
    jaati: "Chatusra",
    speed: "madhyama",
  };
}

// ---------------------------------------------------------------------------
// Main Parser
// ---------------------------------------------------------------------------

/**
 * Parse a RagaNotate ASCII notation string into a NotationAST.
 *
 * @param notation  e.g. "| S R~ G M | P/D N S' ||"
 * @param tala      Tala name override (default: "Adi")
 * @param jaati     Jaati (default: "Chatusra")
 * @param speed     Speed (default: "madhyama")
 *
 * @example
 * ```ts
 * import { parseNotation } from "./parser";
 * const ast = parseNotation("| S R~ G M | P/D N S' ||", "Adi");
 * console.log(ast.nodes.length);
 * ```
 */
export function parseNotation(
  notation: string,
  tala = "Adi",
  jaati = "Chatusra",
  speed: "prathama" | "madhyama" | "durita" = "madhyama",
): NotationAST {

  const tokens = tokenize(notation);

  const ast: NotationAST = {
    tala: parseTalaHeader(tokens) ?? {
      type: "tala",
      name: tala,
      jaati,
      speed,
    },
    nodes: [],
    metadata: { tala, jaati, speed },
  };

  for (const token of tokens) {
    switch (token.kind) {
      case "TALA_HEADER":
      case "COMMENT":
      case "WHITESPACE":
        break;

      case "SECTION_END":
        ast.nodes.push({ type: "bar", isSectionEnd: true } as BarNode);
        break;

      case "BAR":
        ast.nodes.push({ type: "bar", isSectionEnd: false } as BarNode);
        break;

      case "HALF_BEAT":
        ast.nodes.push({ type: "half_beat" } as HalfBeatNode);
        break;

      case "REST":
        ast.nodes.push({ type: "rest", duration: 1.0 } as RestNode);
        break;

      case "SWARA": {
        const node = parseSwaraToken(token.value);
        if (node) ast.nodes.push(node);
        break;
      }
    }
  }

  return ast;
}

// ---------------------------------------------------------------------------
// AST Query helpers
// ---------------------------------------------------------------------------

/** Return only SwaraNodes from an AST. */
export function getSwaras(ast: NotationAST): SwaraNode[] {
  return ast.nodes.filter((n): n is SwaraNode => n.type === "swara");
}

/** Split AST nodes into bars (between | markers). */
export function getBars(ast: NotationAST): ASTNode[][] {
  const bars: ASTNode[][] = [];
  let current: ASTNode[] = [];
  for (const node of ast.nodes) {
    if (node.type === "bar") {
      if (current.length > 0) bars.push(current);
      current = [];
    } else {
      current.push(node);
    }
  }
  if (current.length > 0) bars.push(current);
  return bars;
}

/** Compute total duration of an AST in aksharas. */
export function totalDuration(ast: NotationAST): number {
  return ast.nodes.reduce((sum, n) => {
    if (n.type === "swara" || n.type === "rest") return sum + n.duration;
    return sum;
  }, 0);
}

/** Annotate AST swaras with lyric syllables. */
export function annotateWithLyrics(
  ast: NotationAST,
  syllables: string[],
): NotationAST {
  let i = 0;
  const annotated = { ...ast };
  annotated.nodes = ast.nodes.map(node => {
    if (node.type === "swara" && i < syllables.length) {
      return { ...node, lyric: syllables[i++] };
    }
    return node;
  });
  return annotated;
}
