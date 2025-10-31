import sys
import time
from typing import Optional

import mido
from mido import MidiFile

def list_midi_output_ports() -> list[str]:
    """Devuelve la lista de puertos de salida MIDI disponibles."""
    return mido.get_output_names()

def pick_port(preferred: Optional[str] = None) -> str:
    """
    Selecciona un puerto de salida.
    - Si `preferred` no es None, intenta buscar por coincidencia parcial (case-insensitive).
    - Si no encuentra, retorna el primer puerto disponible.
    """
    ports = list_midi_output_ports()
    if not ports:
        raise RuntimeError(
            "No hay puertos MIDI de salida. Crea uno virtual y habilítalo en Reaper."
        )
    if preferred:
        preferred_low = preferred.lower()
        for p in ports:
            if preferred_low in p.lower():
                return p
        raise RuntimeError(
            f"No encontré un puerto que contenga: '{preferred}'. Puertos disponibles:\n  - " +
            "\n  - ".join(ports)
        )
    return ports[0]

def play_midi_via_port(midi_path: str, out_port_name: Optional[str] = None):
    """
    Reproduce un archivo MIDI enviándolo a un puerto de salida.
    - `midi_path`: ruta al .mid recién creado.
    - `out_port_name`: nombre (o parte del nombre) del puerto MIDI (ej. 'KivyOut', 'IAC Driver', 'loopMIDI').
    """
    port_name = pick_port(out_port_name)
    print(f"Usando puerto de salida: {port_name}")

    # Carga el archivo y usa el generador .play() para respetar tiempos/tempo
    mid = MidiFile(midi_path, clip=True)

    # Abre el puerto y envía eventos con tiempos correctos
    with mido.open_output(port_name) as out:
        start = time.time()
        for msg in mid.play():  # .play() duerme internamente según el delta-time/tempo
            if not msg.is_meta:
                out.send(msg)

    dur = time.time() - start
    print(f"Reproducción terminada. Duración ~{dur:.2f}s")


def midi_duration_seconds(midi_path: str, default_tempo: int = 500_000) -> float:
    """
    Devuelve la duración total en segundos del archivo MIDI,
    respetando cambios de tempo.
    """
    mid = mido.MidiFile(midi_path)
    tpb = mid.ticks_per_beat
    tempo = default_tempo
    elapsed = 0.0

    for msg in mido.merge_tracks(mid.tracks):
        if msg.time:
            elapsed += mido.tick2second(msg.time, tpb, tempo)
        if msg.type == 'set_tempo':
            tempo = msg.tempo
    return elapsed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python play_to_reaper.py <ruta_al_mid> [nombre_parcial_del_puerto]")
        print("Ejemplo: python play_to_reaper.py output.mid KivyOut")
        sys.exit(1)

    midi_file = sys.argv[1]
    port_hint = sys.argv[2] if len(sys.argv) >= 3 else None

    print("Puertos de salida disponibles:")
    for p in list_midi_output_ports():
        print(" -", p)

    play_midi_via_port(midi_file, port_hint)

