/**
 * tala.ts — Tala Definitions & Beat Pattern Generator
 * =====================================================
 * All Suladi Sapta Talas + Chapu + beat clock utilities.
 *
 * github.com/jags111/RagaNotate
 */

import type { Anga, TalaDefinition } from "./types";

// ---------------------------------------------------------------------------
// Anga builders
// ---------------------------------------------------------------------------
const laghu  = (jaati = 4):  Anga => ({ type: "l", jaati, aksharas: jaati });
const dhrutam = ():           Anga => ({ type: "O", jaati: 0, aksharas: 2  });
const anudhrutam = ():        Anga => ({ type: "U", jaati: 0, aksharas: 1  });

// ---------------------------------------------------------------------------
// Suladi Sapta Talas
// ---------------------------------------------------------------------------
export const TALAS: Record<string, TalaDefinition> = {

  Dhruva: {
    name: "Dhruva",
    angas: [laghu(), dhrutam(), laghu(), laghu()],
    totalAksharas: 14,
    description: "l O l l = 14 aksharas (Chatusra)",
  },

  Matya: {
    name: "Matya",
    angas: [laghu(3), dhrutam(), laghu(3)],
    totalAksharas: 9,
    description: "l O l = 3+2+3 = 9 aksharas (Tisra)",
  },

  Rupaka: {
    name: "Rupaka",
    angas: [dhrutam(), laghu()],
    totalAksharas: 6,
    description: "O l = 2+4 = 6 aksharas",
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
    description: "l O O = 4+2+2 = 8 aksharas",
  },

  Ata: {
    name: "Ata",
    angas: [laghu(), laghu(), dhrutam(), dhrutam()],
    totalAksharas: 14,
    description: "l l O O = 4+4+2+2 = 14 aksharas",
  },

  Eka: {
    name: "Eka",
    angas: [laghu()],
    totalAksharas: 4,
    description: "l = 4 aksharas",
  },

  Adi: {
    name: "Adi",
    angas: [laghu(4), dhrutam(), dhrutam()],
    totalAksharas: 8,
    description: "Chatusra Jati Triputa = l4 O O = 8 aksharas (most common)",
  },
};

// ---------------------------------------------------------------------------
// Chapu Talas
// ---------------------------------------------------------------------------
export const CHAPU_TALAS: Record<string, { beats: number; pattern: string; solkattu: string }> = {
  Thisra_Chapu:    { beats: 3, pattern: "1+2", solkattu: "Tha-Ki-Ta" },
  Khanda_Chapu:    { beats: 5, pattern: "2+3", solkattu: "Tha-Ka-Tha-Ki-Ta" },
  Misra_Chapu:     { beats: 7, pattern: "3+4", solkattu: "Tha-Ki-Ta-Tha-Ka-Dhi-Mi" },
  Sankeerna_Chapu: { beats: 9, pattern: "4+5", solkattu: "Tha-Ka-Dhi-Mi-Tha-Ka-Tha-Ki-Ta" },
};

// ---------------------------------------------------------------------------
// Beat Clock
// ---------------------------------------------------------------------------
export interface BeatEvent {
  akshara:     number;
  timeS:       number;
  anga:        Anga;
  angaIndex:   number;
  beatInAnga:  number;
  isAngaStart: boolean;
}

export function* generateBeats(
  tala: TalaDefinition,
  bpm: number,
): Generator<BeatEvent> {
  const beatDur = 60.0 / bpm;
  let akshara = 0;

  for (let angaIdx = 0; angaIdx < tala.angas.length; angaIdx++) {
    const anga = tala.angas[angaIdx];
    for (let beat = 0; beat < anga.aksharas; beat++) {
      yield {
        akshara,
        timeS:       akshara * beatDur,
        anga,
        angaIndex:   angaIdx,
        beatInAnga:  beat,
        isAngaStart: beat === 0,
      };
      akshara++;
    }
  }
}

export function getTala(name: string): TalaDefinition {
  const key = Object.keys(TALAS).find(
    (k) => k.toLowerCase() === name.toLowerCase()
  );
  if (!key) {
    throw new Error(`Unknown tala: "${name}". Available: ${Object.keys(TALAS).join(", ")}`);
  }
  return TALAS[key];
}
