import time
import threading
import mido
from mido import MidiFile

class MidiOutPlayer:
    def __init__(self, port_name: str):
        self.port_name = port_name
        self._stop = threading.Event()
        self._thread = None

    def _sleep_interruptible(self, seconds: float, slice_sec: float = 0.01):
        end = time.time() + seconds
        while not self._stop.is_set() and time.time() < end:
            time.sleep(min(slice_sec, end - time.time()))

    def _panic(self, out):
        # All Notes Off / All Sound Off por seguridad (0-15 canales)
        for ch in range(16):
            out.send(mido.Message('control_change', channel=ch, control=123, value=0))  # All Notes Off
            out.send(mido.Message('control_change', channel=ch, control=120, value=0))  # All Sound Off
            out.send(mido.Message('control_change', channel=ch, control=64, value=0))   # Sustain off

    def play(self, midi_path: str, on_finished=None):
        """Inicia la reproducción en un hilo. Si ya está sonando, detiene y re-inicia."""
        self.stop(wait=True)
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, args=(midi_path, on_finished), daemon=True
        )
        self._thread.start()

    def stop(self, wait: bool = False):
        """Solicita parar. Si wait=True, espera a que cierre el hilo."""
        if self._thread and self._thread.is_alive():
            self._stop.set()
            if wait:
                self._thread.join()

    def _run(self, midi_path: str, on_finished):
        mid = MidiFile(midi_path)
        tpb = mid.ticks_per_beat
        tempo = 500_000  # 120 BPM por defecto

        try:
            with mido.open_output(self.port_name) as out:
                for msg in mido.merge_tracks(mid.tracks):
                    if self._stop.is_set():
                        self._panic(out)
                        return
                    # Espera el delta-time convertido a segundos con el tempo actual
                    wait = mido.tick2second(msg.time, tpb, tempo)
                    if wait > 0:
                        self._sleep_interruptible(wait)
                        if self._stop.is_set():
                            self._panic(out)
                            return
                    # Actualiza tempo o envía el mensaje
                    if msg.type == 'set_tempo':
                        tempo = msg.tempo
                    elif not msg.is_meta:
                        out.send(msg)
                # Terminó normal
                if on_finished and not self._stop.is_set():
                    on_finished()
        finally:
            self._stop.clear()

