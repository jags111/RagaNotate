/**
 * lexer.ts — Notation String Tokenizer
 * =====================================
 * Converts a RagaNotate ASCII notation string into a flat Token[] array.
 * Handles swaras, gamakas, octave markers, duration, tala markers.
 *
 * github.com/jags111/RagaNotate
 */

// ---------------------------------------------------------------------------
// Token Types
// ---------------------------------------------------------------------------
export type TokenKind =
  | "SECTION_END"   // ||
  | "BAR"           // |
  | "HALF_BEAT"     // ,
  | "REST"          // -
  | "SWARA"         // S R G M P D N (with optional prefixes/suffixes)
  | "TALA_HEADER"   // tala: Adi
  | "COMMENT"       // # ... text
  | "WHITESPACE";

export interface Token {
  kind: TokenKind;
  value: string;
  position: number;  // character offset in source
}

// ---------------------------------------------------------------------------
// Token Patterns (order matters — longest first)
// ---------------------------------------------------------------------------
const TOKEN_PATTERNS: Array<{ kind: TokenKind; re: RegExp }> = [
  { kind: "SECTION_END",  re: /\|\|/ },
  { kind: "BAR",          re: /\|/ },
  { kind: "HALF_BEAT",    re: /,/ },
  { kind: "REST",         re: /-/ },
  { kind: "TALA_HEADER",  re: /tala:\s*\w+/i },
  { kind: "COMMENT",      re: /#[^\n]*/ },
  // Swara: optional mandra dot, base letter, optional tara tick, optional variant,
  //        optional duration, optional gamaka
  {
    kind: "SWARA",
    re: /\.?[SRGMPDNsrgmpdn]['+]?[123]?[;:]*(~~|vib|tr|gl|sp|nd|~|\/|\\|v|\^|w|\*|\{[a-z]+\})?/,
  },
  { kind: "WHITESPACE",   re: /\s+/ },
];

// ---------------------------------------------------------------------------
// Lexer
// ---------------------------------------------------------------------------
export function tokenize(source: string): Token[] {
  const tokens: Token[] = [];
  let pos = 0;

  while (pos < source.length) {
    let matched = false;

    for (const { kind, re } of TOKEN_PATTERNS) {
      const result = re.exec(source.slice(pos));
      if (result && result.index === 0) {
        const value = result[0];
        if (kind !== "WHITESPACE" && kind !== "COMMENT") {
          tokens.push({ kind, value, position: pos });
        }
        pos += value.length;
        matched = true;
        break;
      }
    }

    if (!matched) {
      // Skip unknown character
      pos++;
    }
  }

  return tokens;
}

// ---------------------------------------------------------------------------
// Debug helper
// ---------------------------------------------------------------------------
export function printTokens(tokens: Token[]): void {
  console.log(`\n── Tokens (${tokens.length}) ─────────────────────`);
  tokens.forEach((t, i) => {
    console.log(`  [${i.toString().padStart(3, "0")}] ${t.kind.padEnd(14)} ${JSON.stringify(t.value)}`);
  });
}
