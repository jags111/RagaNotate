"""
midi_generator.py — AST → MIDI with Gamaka Pitch Bends
========================================================
Converts a NotationAST into a MIDI file, with:
  - Just Intonation frequency → MIDI note + pitch bend
  - Gamaka pitch contours encoded as pitch bend sequences
  - Tala tempo from BPM

Requires: MIDIUtil (pip install MIDIUtil)
  NOTE: PyPI package name is "MIDIUtil" (capital M and U) — NOT "midiutil" lowercase.

Ref: ARCHITECTURE.md · github.com/jags111/RagaNotate
"""

from __future__ import annotations
import math
from typing import Optional

from .parser import NotationAST, SwaraNode, RestNode
from .swara import swara_hz, DEFAULT_SA_HZ
from .gamaka import PitchCurveType


# ---------------------------------------------------------------------------
# Frequency → MIDI Note + Pitch Bend
# ---------------------------------------------------------------------------

def hz_to_midi(freq_hz: float) -> tuple[int, float]:
    """Convert a frequency (Hz) to MIDI note number and pitch bend cents.

    MIDI uses equal temperament; pitch bend compensates for JI deviations.

    Args:
        freq_hz: Frequency in Hz

    Returns:
        (midi_note, cents_bend) where cents_bend is the fine-tuning offset.
    """
    if freq_hz <= 0:
        return (60, 0.0)
    # A4 = 440 Hz = MIDI note 69
    midi_float = 69.0 + 12.0 * math.log2(freq_hz / 440.0)
    midi_note = round(midi_float)
    cents_bend = (midi_float - midi_note) * 100.0
    return (midi_note, cents_bend)


def cents_to_pitch_bend(cents: float, semitone_range: int = 2) -> int:
    """Convert cents offset to MIDI pitch bend value (-8192 to 8191).

    Args:
        cents:          Fine-tuning in cents (-200 to +200 typical)
        semitone_range: Pitch bend range in semitones (default ±2)

    Returns:
        MIDI pitch bend integer
    """
    max_cents = semitone_range * 100.0
    pb = int((cents / max_cents) * 8191)
    return max(-8192, min(8191, pb))


# ---------------------------------------------------------------------------
# MIDI Generator
# ---------------------------------------------------------------------------

class MidiGenerator:
    """Generates a MIDI file from a NotationAST.

    Usage:
        from raganotate.midi_generator import MidiGenerator
        gen = MidiGenerator(sa_hz=240.0, bpm=80.0)
        gen.generate(ast, output_path="vathapi.mid")
    """

    PITCH_BEND_SEMITONES = 2      # Pitch bend range (±2 semitones recommended)
    GAMAKA_STEPS = 16             # Number of pitch bend steps per gamaka
    CHANNEL = 0                   # MIDI channel (0 = channel 1)
    PROGRAM = 25                  # MIDI program: 25 = Acoustic Guitar (nylon), 40 = Violin

    def __init__(
        self,
        sa_hz: float = DEFAULT_SA_HZ,
        bpm: float = 72.0,
        program: int = 25,
        volume: int = 100,
    ):
        self.sa_hz = sa_hz
        self.bpm = bpm
        self.program = program
        self.volume = volume

    def generate(
        self,
        ast: NotationAST,
        output_path: str = "output.mid",
    ) -> str:
        """Generate a MIDI file from a NotationAST.

        Args:
            ast:         Parsed notation AST
            output_path: Output .mid file path

        Returns:
            output_path on success.

        Raises:
            ImportError if midiutil is not installed.
        """
        try:
            from midiutil import MIDIFile
        except ImportError:
            raise ImportError(
                "MIDIUtil is required: pip install MIDIUtil\n"
                "  (capital M and U — NOT 'midiutil' lowercase)"
            )

        midi = MIDIFile(numTracks=1)
        midi.addTempo(track=0, time=0, tempo=self.bpm)
        midi.addProgramChange(track=0, channel=self.CHANNEL, time=0, program=self.program)

        time = 0.0  # current time in beats (1 beat = 1 akshara)

        for node in ast.nodes:
            if isinstance(node, RestNode):
                time += node.duration

            elif isinstance(node, SwaraNode):
                freq = swara_hz(node.symbol, node.octave, self.sa_hz)
                midi_note, cents = hz_to_midi(freq)
                dur = node.duration

                if node.gamaka is None or node.gamaka.token == "GMK_AHAT":
                    # Plain note
                    pb = cents_to_pitch_bend(cents, self.PITCH_BEND_SEMITONES)
                    midi.addPitchWheelEvent(
                        track=0, channel=self.CHANNEL, time=time, pitchWheelValue=pb
                    )
                    midi.addNote(
                        track=0, channel=self.CHANNEL,
                        pitch=midi_note, time=time,
                        duration=dur, volume=self.volume
                    )
                else:
                    # Gamaka: encode as pitch bend sequence
                    self._add_gamaka_note(
                        midi, node, freq, midi_note, cents, dur, time
                    )

                time += dur

        # Write file
        with open(output_path, "wb") as f:
            midi.writeFile(f)

        return output_path

    def _add_gamaka_note(
        self,
        midi,
        node: SwaraNode,
        freq: float,
        midi_note: int,
        cents: float,
        dur: float,
        start_time: float,
    ) -> None:
        """Add a note with gamaka pitch bend sequence."""
        from midiutil import MIDIFile

        steps = self.GAMAKA_STEPS
        step_dur = dur / steps
        gmk = node.gamaka

        # Get adjacent swara frequency for slides
        onset_freq = freq * 0.95 if gmk.curve_type in (
            PitchCurveType.LINEAR_UP, PitchCurveType.GRACE_UP
        ) else freq * 1.05

        pitch_fn = gmk.pitch_fn(
            onset_hz=onset_freq,
            target_hz=freq,
            duration_s=dur,
        )

        # Add pitch bend events across the duration
        for i in range(steps):
            t = start_time + i * step_dur
            t_local = i * step_dur
            hz_at_t = pitch_fn(t_local)
            _, c = hz_to_midi(hz_at_t)
            pb = cents_to_pitch_bend(c, self.PITCH_BEND_SEMITONES)
            midi.addPitchWheelEvent(
                track=0, channel=self.CHANNEL,
                time=t, pitchWheelValue=pb
            )

        # Add the note itself
        midi.addNote(
            track=0, channel=self.CHANNEL,
            pitch=midi_note, time=start_time,
            duration=dur, volume=self.volume
        )


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def ast_to_midi(
    ast: NotationAST,
    output_path: str = "output.mid",
    sa_hz: float = DEFAULT_SA_HZ,
    bpm: float = 72.0,
    program: int = 25,
) -> str:
    """Generate a MIDI file from a NotationAST in one call.

    Args:
        ast:         Parsed NotationAST
        output_path: Output .mid file path
        sa_hz:       Adhara Shadjam Hz
        bpm:         Tempo (beats per minute)
        program:     MIDI instrument program number

    Returns:
        output_path string.
    """
    gen = MidiGenerator(sa_hz=sa_hz, bpm=bpm, program=program)
    return gen.generate(ast, output_path)


# ---------------------------------------------------------------------------
# Main — demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from .parser import parse_notation

    notation = "| S R G M | P D N S' | N D P M | G R S ||"
    ast = parse_notation(notation, tala="Adi")

    try:
        path = ast_to_midi(ast, "test_output.mid", sa_hz=240.0, bpm=72.0)
        print(f"MIDI written to: {path}")
    except ImportError as e:
        print(f"Install MIDIUtil first: pip install MIDIUtil")
        print(f"  {e}")
