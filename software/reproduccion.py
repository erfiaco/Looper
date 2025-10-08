import sounddevice as sd
from threading import Thread, Event
from software.audio_clip import AudioClip
import numpy as np

class LooperReproduccion:
    def __init__(self, ultimo_clip=None, on_state_change=None):
        self.ultimo_clip = ultimo_clip
        self.reproduciendo = False
        self.stop_event = Event()
        self.playback_thread = None
        self.on_state_change = on_state_change

    def start_loop(self):
        """Inicia reproducción en bucle."""
        if not self.ultimo_clip or not self.ultimo_clip.datos.size:
            if self.on_state_change:
                self.on_state_change("No hay clip para reproducir")
            return
        self.reproduciendo = True
        self.stop_event.clear()
        if self.on_state_change:
            self.on_state_change("Reproduciendo")
        self.playback_thread = Thread(target=self._reproducir_en_bucle)
        self.playback_thread.daemon = True
        self.playback_thread.start()

    def _reproducir_en_bucle(self):
        """Hilo para bucle infinito."""
        data = self.ultimo_clip.datos.astype(np.float32)
        fs = self.ultimo_clip.SAMPLE_RATE
        while self.reproduciendo and not self.stop_event.is_set():
            sd.play(data, fs)
            sd.wait()  # Espera reproducción; no bloquea main por daemon
        sd.stop()
        self.reproduciendo = False
        if self.on_state_change:
            self.on_state_change("Reproducción detenida")

    def stop(self):
        """Detiene reproducción."""
        self.reproduciendo = False
        self.stop_event.set()
        if self.playback_thread:
            self.playback_thread.join(timeout=1)

    def set_clip(self, clip):
        """Asigna nuevo clip."""
        self.ultimo_clip = clip