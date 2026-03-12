/**
 * tala.ts — Tala Definitions & Beat Pattern Engine
 * ==================================================
 * Full TypeScript port of Python's TalaEngine, including:
 *   - All Suladi Sapta Talas (8 ragas including Adi)
 *   - 4 Chapu Talas
 *   - TalaEngine class: cycle iteration, avartana tracking, callbacks
 *   - Beat pattern generators (one-shot + continuous)
 *   - Validation helpers
 *
 * Ref: RagaNotate SPEC.md §7 · github.com/jags111/RagaNotate
 */

import type { Anga, TalaDefinition } from "./types";

// ---------------------------------------------------------------------------
// Anga builders
// ---------------------------------------------------------------------------

const laghu      = (jaati = 4): Anga => ({ type: "l", jaati, aksharas: jaati });
const dhrutam    = ():           Anga => ({ type: "O", jaati: 0, aksharas: 2 });
const anudhrutam = ():           Anga => ({ type: "U", jaati: 0, aksharas: 1 });

// ---------------------------------------------------------------------------
// Suladi Sapta Talas
// ---------------------------------------------------------------------------

export const TALAS: Record<string, TalaDefinition> = {

  Dhruva: {
    name: "Dhruva",
    angas: [laghu(), dhrutam(), laghu(), laghu()],
    totalAksharas: 14,
    description: "l O l l = 4+2+4+4 = 14 aksharas (Chatusra Jati)",
  },

  Matya: {
    name: "Matya",
    angas: [laghu(3), dhrutam(), laghu(3)],
    totalAksharas: 8,
    description: "l O l = 3+2+3 = 8 aksharas (Tisra Jati)",
  },

  Rupaka: {
    name: "Rupaka",
    angas: [dhrutam(), laghu()],
    totalAksharas: 6,
    description: "O l = 2+4 = 6 aksharas (Chatusra Jati)",
  },

  Jhampa: {
    name: "Jhampa",
    angas: [laghu(7), anudhrutam(), dhrutam()],
    totalAksharas: 10,
    description: "l U O = 7+1+2 = 10 aksharas (Misra Laghu)",
  },

  Triputa: {
    name: "Triputa",
    angas: [laghu(), dhrutam(), dhrutam()],
    totalAksharas: 8,
    description: "l O O = 4+2+2 = 8 aksharas (Chatusra Jati)",
  },

  Ata: {
    name: "Ata",
    angas: [laghu(), laghu(), dhrutam(), dhrutam()],
    totalAksharas: 14,
    description: "l l O O = 4+4+2+2 = 14 aksharas (Chatusra Jati)",
  },

  Eka: {
    name: "Eka",
    angas: [laghu()],
    totalAksharas: 4,
    description: "l = 4 aksharas (Chatusra Jati)",
  },

  /** Adi = Chatusra Jati Triputa — the most common tala in Carnatic music */
  Adi: {
    name: "Adi",
    angas: [laghu(4), dhrutam(), dhrutam()],
    totalAksharas: 8,
    description: "Chatusra Jati Triputa = l4 O O = 8 aksharas",
  },
};

// ---------------------------------------------------------------------------
// Chapu Talas
// ---------------------------------------------------------------------------

export interface ChapuTala {
  name: string;
  beats: number;
  pattern: string;       // e.g. "2+3"
  solkattu: string;
  grouping: number[];    // beat-group sizes, sums to beats
}

export const CHAPU_TALAS: Record<string, ChapuTala> = {
  Thisra_Chapu: {
    name: "Thisra Chapu",
    beats: 3,
    pattern: "1+2",
    solkattu: "Tha-Ki-Ta",
    grouping: [1, 2],
  },
  Khanda_Chapu: {
    name: "Khanda Chapu",
    beats: 5,
    pattern: "2+3",
    solkattu: "Tha-Ka-Tha-Ki-Ta",
    grouping: [2, 3],
  },
  Misra_Chapu: {
    name: "Misra Chapu",
    beats: 7,
    pattern: "3+4",
    solkattu: "Tha-Ki-Ta-Tha-Ka-Dhi-Mi",
    grouping: [3, 4],
  },
  Sankeerna_Chapu: {
    name: "Sankeerna Chapu",
    beats: 9,
    pattern: "4+5",
    solkattu: "Tha-Ka-Dhi-Mi-Tha-Ka-Tha-Ki-Ta",
    grouping: [4, 5],
  },
};

// ---------------------------------------------------------------------------
// Beat Event
// ---------------------------------------------------------------------------

export interface BeatEvent {
  /** Zero-based akshara index within the avartana (0 … totalAksharas-1) */
  akshara:       number;
  /** Absolute wall-clock offset in seconds from avartana start */
  timeS:         number;
  /** The Anga this akshara belongs to */
  anga:          Anga;
  /** Index of anga within tala definition (0-based) */
  angaIndex:     number;
  /** Beat position within the anga (0-based) */
  beatInAnga:    number;
  /** True on the first akshara of each anga */
  isAngaStart:   boolean;
  /** True only on akshara 0 (Sam) */
  isSam:         boolean;
  /** Avartana (cycle) number, 0-based */
  avartana:      number;
  /** Human-readable label, e.g. "Laghu beat 1", "Drutam Sam" */
  label:         string;
}

// ---------------------------------------------------------------------------
// Anga label helpers
// ---------------------------------------------------------------------------

function angaName(anga: Anga): string {
  switch (anga.type) {
    case "l": return "Laghu";
    case "O": return "Drutam";
    case "U": return "Anudhrutam";
    case "8": return "Guru";
    case ")": return "Plutam";
    case "+": return "Kakapadam";
    default:  return "Anga";
  }
}

function beatLabel(anga: Anga, beatInAnga: number, isSam: boolean): string {
  if (isSam) return "Sam (Thom)";
  const name = angaName(anga);
  return `${name} beat ${beatInAnga + 1}`;
}

// ---------------------------------------------------------------------------
// One-shot beat pattern generator (for one avartana)
// ---------------------------------------------------------------------------

/**
 * Generator that yields every BeatEvent in a single avartana (one cycle).
 * Use in `for…of` loops or spread to an array.
 *
 * @example
 *   const events = [...generateBeats(TALAS.Adi, 80)];
 *   // → 8 BeatEvent objects, timeS from 0 to 4.9s at 80 BPM
 */
export function* generateBeats(
  tala: TalaDefinition,
  bpm: number,
  avartana = 0,
): Generator<BeatEvent> {
  const beatDurS = 60.0 / bpm;
  let akshara = 0;

  for (let angaIdx = 0; angaIdx < tala.angas.length; angaIdx++) {
    const anga = tala.angas[angaIdx];
    for (let beat = 0; beat < anga.aksharas; beat++) {
      const isSam = akshara === 0;
      yield {
        akshara,
        timeS:       akshara * beatDurS,
        anga,
        angaIndex:   angaIdx,
        beatInAnga:  beat,
        isAngaStart: beat === 0,
        isSam,
        avartana,
        label:       beatLabel(anga, beat, isSam),
      };
      akshara++;
    }
  }
}

// ---------------------------------------------------------------------------
// TalaEngine — stateful beat clock with callbacks
// ---------------------------------------------------------------------------

export type BeatCallback = (event: BeatEvent) => void;
export type AvartanaCallback = (avartana: number) => void;

export interface TalaEngineOptions {
  /** Tala to use (from TALAS or custom) */
  tala: TalaDefinition;
  /** Beats per minute (aksharas per minute) */
  bpm: number;
  /** Called on every akshara */
  onBeat?: BeatCallback;
  /** Called at the start of each new avartana (akshara 0) */
  onAvartana?: AvartanaCallback;
  /** Maximum number of avartanas to run (default: unlimited) */
  maxAvartanas?: number;
}

/**
 * TalaEngine — stateful, callback-based beat clock.
 *
 * Matches the Python TalaEngine API:
 *   engine.start()  — begin ticking
 *   engine.stop()   — pause
 *   engine.reset()  — back to avartana 0, akshara 0
 *   engine.tick()   — advance one akshara manually (useful for testing)
 *
 * Uses `setInterval` for real-time playback when running in a browser.
 * In Node.js, use `tick()` manually.
 *
 * @example
 *   const engine = new TalaEngine({
 *     tala: TALAS.Adi,
 *     bpm: 80,
 *     onBeat: (e) => console.log(e.label),
 *     onAvartana: (n) => console.log(`Avartana ${n + 1}`),
 *   });
 *   engine.start();   // real-time via setInterval
 *   setTimeout(() => engine.stop(), 5000);
 */
export class TalaEngine {
  private tala:          TalaDefinition;
  private bpm:           number;
  private onBeat?:       BeatCallback;
  private onAvartana?:   AvartanaCallback;
  private maxAvartanas:  number;

  private _akshara:      number = 0;
  private _avartana:     number = 0;
  private _running:      boolean = false;
  private _intervalId:   ReturnType<typeof setInterval> | null = null;

  /** Pre-computed flat beat sequence for current avartana */
  private _beatSeq:      BeatEvent[] = [];

  constructor(opts: TalaEngineOptions) {
    this.tala         = opts.tala;
    this.bpm          = opts.bpm;
    this.onBeat       = opts.onBeat;
    this.onAvartana   = opts.onAvartana;
    this.maxAvartanas = opts.maxAvartanas ?? Infinity;
    this._buildBeatSeq();
  }

  // ── Public API ────────────────────────────────────────────────────────────

  get akshara():  number  { return this._akshara; }
  get avartana(): number  { return this._avartana; }
  get running():  boolean { return this._running; }
  get bpmValue(): number  { return this.bpm; }

  /** Current beat event (the last one fired, or the first before start). */
  get currentBeat(): BeatEvent {
    return this._beatSeq[this._akshara] ?? this._beatSeq[0];
  }

  /** Milliseconds per akshara at current BPM. */
  get aksharaMs(): number {
    return (60_000 / this.bpm);
  }

  /** Start real-time ticking using setInterval. */
  start(): void {
    if (this._running) return;
    this._running = true;
    this._intervalId = setInterval(() => this.tick(), this.aksharaMs);
  }

  /** Pause ticking (preserves position). */
  stop(): void {
    this._running = false;
    if (this._intervalId !== null) {
      clearInterval(this._intervalId);
      this._intervalId = null;
    }
  }

  /** Reset position back to avartana 0, akshara 0. Does NOT stop. */
  reset(): void {
    this._akshara  = 0;
    this._avartana = 0;
    this._buildBeatSeq();
  }

  /** Change BPM on the fly (restarts interval if running). */
  setBpm(bpm: number): void {
    const wasRunning = this._running;
    if (wasRunning) this.stop();
    this.bpm = bpm;
    if (wasRunning) this.start();
  }

  /**
   * Advance one akshara manually.
   * Fires `onBeat` and `onAvartana` callbacks exactly as real-time ticking does.
   * Useful for unit tests and non-browser environments.
   */
  tick(): void {
    const event = this._beatSeq[this._akshara];
    if (!event) return;

    if (event.isSam && this.onAvartana) {
      this.onAvartana(this._avartana);
    }
    if (this.onBeat) {
      this.onBeat({ ...event, avartana: this._avartana });
    }

    this._akshara++;
    if (this._akshara >= this.tala.totalAksharas) {
      this._akshara = 0;
      this._avartana++;
      this._buildBeatSeq();  // refresh with new avartana number
      if (this._avartana >= this.maxAvartanas) {
        this.stop();
      }
    }
  }

  /**
   * Run synchronously for N avartanas and return all BeatEvents.
   * Does NOT use setInterval — returns immediately.
   * Useful for generating notation grids, audio scheduling, etc.
   *
   * @example
   *   const allBeats = engine.runSync(2);  // 2 avartanas × 8 = 16 beats for Adi
   */
  runSync(avartanas = 1): BeatEvent[] {
    const events: BeatEvent[] = [];
    for (let av = 0; av < avartanas; av++) {
      for (const e of generateBeats(this.tala, this.bpm, av)) {
        events.push(e);
      }
    }
    return events;
  }

  /**
   * Return the full beat sequence for ONE avartana as a plain array.
   * Each element carries the absolute timeS offset (from cycle start).
   */
  oneBeatCycle(avartana = 0): BeatEvent[] {
    return [...generateBeats(this.tala, this.bpm, avartana)];
  }

  // ── Private helpers ───────────────────────────────────────────────────────

  private _buildBeatSeq(): void {
    this._beatSeq = [...generateBeats(this.tala, this.bpm, this._avartana)];
  }
}

// ---------------------------------------------------------------------------
// Utility: get tala by name (case-insensitive)
// ---------------------------------------------------------------------------

export function getTala(name: string): TalaDefinition {
  const key = Object.keys(TALAS).find(
    (k) => k.toLowerCase() === name.toLowerCase()
  );
  if (!key) {
    throw new Error(
      `Unknown tala: "${name}". Available: ${Object.keys(TALAS).join(", ")}`
    );
  }
  return TALAS[key];
}

// ---------------------------------------------------------------------------
// Utility: validate a notation bar against tala
// ---------------------------------------------------------------------------

export interface BarValidation {
  valid: boolean;
  expected: number;
  actual: number;
  shortfall: number;   // > 0 means bar is short; < 0 means bar is long
  message: string;
}

/**
 * Validate that a bar's total duration (in aksharas) matches the tala.
 *
 * @param barDuration  Total aksharas counted in the bar
 * @param tala         TalaDefinition to validate against
 */
export function validateBar(
  barDuration: number,
  tala: TalaDefinition,
): BarValidation {
  const expected = tala.totalAksharas;
  const shortfall = expected - barDuration;
  const valid = shortfall === 0;
  return {
    valid,
    expected,
    actual: barDuration,
    shortfall,
    message: valid
      ? `Bar duration ${barDuration} matches ${tala.name} (${expected} aksharas) ✓`
      : shortfall > 0
        ? `Bar is SHORT by ${shortfall} akshara(s): got ${barDuration}, expected ${expected} for ${tala.name}`
        : `Bar is LONG by ${-shortfall} akshara(s): got ${barDuration}, expected ${expected} for ${tala.name}`,
  };
}

// ---------------------------------------------------------------------------
// Utility: print tala beat pattern to console (debugging)
// ---------------------------------------------------------------------------

export function printTalaPattern(tala: TalaDefinition, bpm = 80): void {
  const events = [...generateBeats(tala, bpm, 0)];
  const sep = "─".repeat(60);
  console.log(`\n${sep}`);
  console.log(`  ${tala.name} Tala — ${tala.totalAksharas} aksharas @ ${bpm} BPM`);
  console.log(`  ${tala.description}`);
  console.log(sep);
  console.log(
    `  ${"Akshara".padEnd(9)}${"Time(s)".padEnd(10)}${"Anga".padEnd(14)}${"Beat".padEnd(7)}Label`
  );
  console.log(`  ${"─".repeat(7).padEnd(9)}${"─".repeat(7).padEnd(10)}${"─".repeat(12).padEnd(14)}${"─".repeat(5).padEnd(7)}${"─".repeat(16)}`);
  for (const e of events) {
    console.log(
      `  ${String(e.akshara + 1).padEnd(9)}${e.timeS.toFixed(3).padEnd(10)}${angaName(e.anga).padEnd(14)}${String(e.beatInAnga + 1).padEnd(7)}${e.label}`
    );
  }
  console.log(`${sep}\n`);
}

// ---------------------------------------------------------------------------
// Module self-test (run with: npx ts-node tala.ts)
// ---------------------------------------------------------------------------

if (typeof require !== "undefined" && require.main === module) {
  // Print all talas
  for (const name of Object.keys(TALAS)) {
    printTalaPattern(TALAS[name], 80);
  }

  // Demo TalaEngine synchronous run
  const engine = new TalaEngine({
    tala: TALAS.Adi,
    bpm: 80,
    onBeat:     (e) => console.log(`  [${e.avartana}:${e.akshara}] ${e.label} @ ${e.timeS.toFixed(2)}s`),
    onAvartana: (n) => console.log(`\n=== Avartana ${n + 1} ===`),
  });

  console.log("\nAdi Tala — 2 avartanas sync run:");
  const beats = engine.runSync(2);
  console.log(`  Total beats: ${beats.length} (expected ${TALAS.Adi.totalAksharas * 2})`);

  // Validate a correct bar
  const v1 = validateBar(8, TALAS.Adi);
  console.log(`\nValidation (8 aksharas / Adi): ${v1.message}`);
  const v2 = validateBar(6, TALAS.Adi);
  console.log(`Validation (6 aksharas / Adi): ${v2.message}`);
}
