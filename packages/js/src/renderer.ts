/**
 * renderer.ts — NotationAST → SVG Visual Notation
 * =================================================
 * Renders a RagaNotate AST as an SVG string.
 * Architecture inspired by srikumarks/carnot.
 *
 * Features:
 *  - Swara boxes with symbol + gamaka indicator
 *  - Octave dots (mandra below, tara above)
 *  - Duration stretching (double/half-width cells)
 *  - Bar lines and half-beat markers
 *  - Optional lyric text below each swara
 *  - Optional tala grid with anga labels
 *  - Light and dark themes
 *
 * Usage:
 *   import { renderSVG } from "./renderer";
 *   const svg = renderSVG(ast, { showLyrics: true, theme: "dark" });
 *   document.getElementById("notation").innerHTML = svg;
 *
 * github.com/jags111/RagaNotate · Inspired by: github.com/srikumarks/carnot
 */

import type {
  NotationAST,
  SwaraNode,
  RestNode,
  BarNode,
  ASTNode,
  RenderOptions,
} from "./types";

// ---------------------------------------------------------------------------
// Default options
// ---------------------------------------------------------------------------
const DEFAULTS: Required<RenderOptions> = {
  width:        900,
  cellWidth:    52,
  cellHeight:   56,
  fontSize:     15,
  showLyrics:   true,
  showTalaGrid: true,
  theme:        "dark",
};

// ---------------------------------------------------------------------------
// Theme palettes
// ---------------------------------------------------------------------------
const THEMES = {
  dark: {
    bg:        "#0f0e17",
    cell:      "#1e1d35",
    border:    "#2d2c4e",
    text:      "#fffffe",
    subtext:   "#a7a9be",
    accent:    "#e8b86d",
    gamakaClr: "#4ecdc4",
    barLine:   "#e8b86d",
    lyric:     "#c97d4e",
    rest:      "#444",
    taraClr:   "#9b59b6",
    mandraClr: "#3498db",
  },
  light: {
    bg:        "#f8f7f2",
    cell:      "#ffffff",
    border:    "#cccccc",
    text:      "#1a1a2e",
    subtext:   "#666688",
    accent:    "#b5862a",
    gamakaClr: "#1a9e98",
    barLine:   "#b5862a",
    lyric:     "#8a4a20",
    rest:      "#bbbbbb",
    taraClr:   "#7b2fa8",
    mandraClr: "#1a6bb0",
  },
};

// ---------------------------------------------------------------------------
// SVG helpers
// ---------------------------------------------------------------------------
function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function rect(
  x: number, y: number, w: number, h: number,
  fill: string, stroke: string, r = 4,
): string {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" ry="${r}" fill="${fill}" stroke="${stroke}" stroke-width="1"/>`;
}

function text(
  x: number, y: number, content: string,
  fill: string, size: number,
  anchor = "middle", weight = "normal",
): string {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="'Courier New',monospace" font-size="${size}" font-weight="${weight}" fill="${fill}">${esc(content)}</text>`;
}

function line(
  x1: number, y1: number, x2: number, y2: number,
  stroke: string, width = 1.5,
): string {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}"/>`;
}

// ---------------------------------------------------------------------------
// Cell renderers
// ---------------------------------------------------------------------------

function renderSwaraCell(
  sw: SwaraNode,
  x: number, y: number,
  cellW: number, cellH: number,
  opts: Required<RenderOptions>,
  palette: typeof THEMES["dark"],
): string {
  const parts: string[] = [];
  const cx = x + cellW / 2;

  // Cell background
  parts.push(rect(x + 2, y + 2, cellW - 4, cellH - 4, palette.cell, palette.border));

  // Tara dot (small circle above symbol)
  if (sw.octave === "tara") {
    parts.push(
      `<circle cx="${cx}" cy="${y + 8}" r="3" fill="${palette.taraClr}"/>`
    );
  }

  // Mandra dot (small circle below symbol)
  if (sw.octave === "mandra") {
    parts.push(
      `<circle cx="${cx}" cy="${y + cellH - 10}" r="3" fill="${palette.mandraClr}"/>`
    );
  }

  // Main swara symbol
  const symbolY = y + cellH / 2 + 5;
  parts.push(text(cx, symbolY, sw.symbol, palette.text, opts.fontSize + 2, "middle", "bold"));

  // Gamaka indicator (top-right corner)
  if (sw.gamaka && sw.gamaka.token !== "GMK_AHAT" && sw.gamaka.symbol) {
    parts.push(text(
      x + cellW - 6, y + 14,
      sw.gamaka.symbol,
      palette.gamakaClr,
      opts.fontSize - 3,
      "end",
    ));
  }

  // Duration indicator (bottom-right, only if != 1)
  if (sw.duration !== 1.0) {
    const durLabel = sw.duration === 2.0 ? "×2" :
                     sw.duration === 0.5 ? "½"  :
                     sw.duration === 0.25 ? "¼" : `×${sw.duration}`;
    parts.push(text(
      x + cellW - 5, y + cellH - 5,
      durLabel,
      palette.subtext,
      opts.fontSize - 4,
      "end",
    ));
  }

  // Lyric text below cell
  if (opts.showLyrics && sw.lyric) {
    parts.push(text(cx, y + cellH + 14, sw.lyric, palette.lyric, opts.fontSize - 2));
  }

  return parts.join("\n");
}

function renderRestCell(
  _node: RestNode,
  x: number, y: number,
  cellW: number, cellH: number,
  opts: Required<RenderOptions>,
  palette: typeof THEMES["dark"],
): string {
  const cx = x + cellW / 2;
  return [
    rect(x + 2, y + 2, cellW - 4, cellH - 4, palette.bg, palette.border),
    text(cx, y + cellH / 2 + 5, "—", palette.rest, opts.fontSize + 2, "middle"),
  ].join("\n");
}

function renderBarLine(
  x: number, y: number, cellH: number,
  isSection: boolean,
  palette: typeof THEMES["dark"],
): string {
  const strokeW = isSection ? 3 : 1.5;
  const parts = [line(x, y, x, y + cellH, palette.barLine, strokeW)];
  if (isSection) {
    parts.push(line(x + 4, y, x + 4, y + cellH, palette.barLine, 1));
  }
  return parts.join("\n");
}

// ---------------------------------------------------------------------------
// Main SVG renderer
// ---------------------------------------------------------------------------

export function renderSVG(
  ast: NotationAST,
  options: RenderOptions = {},
): string {
  const opts: Required<RenderOptions> = { ...DEFAULTS, ...options };
  const palette = THEMES[opts.theme];

  const cellW = opts.cellWidth;
  const cellH = opts.cellHeight;
  const padX = 16;
  const padY = 16;
  const lyricH = opts.showLyrics ? 20 : 0;
  const talaH  = opts.showTalaGrid ? 20 : 0;
  const rowH   = cellH + lyricH + talaH;

  // Pre-compute total width and wrap rows
  const CELLS_PER_ROW = Math.floor((opts.width - padX * 2) / cellW);

  // Flatten non-bar nodes into visual cells
  type VisualCell =
    | { kind: "swara"; node: SwaraNode }
    | { kind: "rest";  node: RestNode }
    | { kind: "bar";   isSection: boolean }
    | { kind: "halfbeat" };

  const cells: VisualCell[] = [];
  for (const node of ast.nodes) {
    if (node.type === "swara")     cells.push({ kind: "swara", node });
    else if (node.type === "rest") cells.push({ kind: "rest",  node });
    else if (node.type === "bar")  cells.push({ kind: "bar",   isSection: (node as BarNode).isSectionEnd });
    else if (node.type === "half_beat") cells.push({ kind: "halfbeat" });
  }

  // Split into rows
  const rows: VisualCell[][] = [];
  let current: VisualCell[] = [];
  let colCount = 0;

  for (const cell of cells) {
    if (cell.kind === "bar") {
      current.push(cell);
    } else {
      if (colCount >= CELLS_PER_ROW && current.length > 0) {
        rows.push(current);
        current = [];
        colCount = 0;
      }
      current.push(cell);
      colCount++;
    }
  }
  if (current.length > 0) rows.push(current);

  const totalH = padY * 2 + rows.length * (rowH + 8) + talaH + 30;

  const parts: string[] = [];

  // SVG header
  parts.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${opts.width}" height="${totalH}" ` +
    `viewBox="0 0 ${opts.width} ${totalH}" style="font-family:'Courier New',monospace">`
  );

  // Background
  parts.push(`<rect width="${opts.width}" height="${totalH}" fill="${palette.bg}"/>`);

  // Title / tala header
  const talaName = ast.tala?.name ?? "—";
  parts.push(text(padX, padY + 12, `♩ ${talaName} Tala`, palette.accent, opts.fontSize, "start", "bold"));

  // Rows
  rows.forEach((row, rowIdx) => {
    const rowY = padY + 28 + rowIdx * (rowH + 8);
    let colX = padX;

    // Tala grid background stripe
    if (opts.showTalaGrid) {
      parts.push(
        `<rect x="${padX}" y="${rowY}" width="${opts.width - padX * 2}" height="${cellH}" ` +
        `rx="4" fill="${palette.border}" opacity="0.3"/>`
      );
    }

    for (const cell of row) {
      if (cell.kind === "bar") {
        parts.push(renderBarLine(colX, rowY, cellH, cell.isSection, palette));
        colX += cell.isSection ? 8 : 4;
      } else if (cell.kind === "halfbeat") {
        parts.push(text(colX + 4, rowY + cellH / 2 + 5, ",", palette.subtext, opts.fontSize));
        colX += 10;
      } else if (cell.kind === "swara") {
        const w = cellW * cell.node.duration;
        parts.push(renderSwaraCell(cell.node, colX, rowY, w, cellH, opts, palette));
        colX += w;
      } else if (cell.kind === "rest") {
        parts.push(renderRestCell(cell.node, colX, rowY, cellW, cellH, opts, palette));
        colX += cellW;
      }
    }
  });

  parts.push("</svg>");
  return parts.join("\n");
}

// ---------------------------------------------------------------------------
// Utility: render to HTML file string
// ---------------------------------------------------------------------------
export function renderHTML(ast: NotationAST, options: RenderOptions = {}): string {
  const svg = renderSVG(ast, options);
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RagaNotate — ${ast.tala?.name ?? "Notation"}</title>
<style>
  body { background: #0f0e17; margin: 0; padding: 24px; }
  svg  { display: block; max-width: 100%; }
</style>
</head>
<body>${svg}</body>
</html>`;
}
