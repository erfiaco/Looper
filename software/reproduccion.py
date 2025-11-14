import sounddevice as sd
import numpy as np
from threading import Thread
from software.audio_clip import AudioClip
from libs import paths
import os

class LooperReproduccion:
    def __init__(self, on_state_change=None):
        self.ultimo_clip = None
        self.reproduciendo = False
        self.stop_event = None
        self.playback_thread = None
        self.on_state_change = on_state_change
        self._cargar_ultimo_archivo()

    def _cargar_ultimo_archivo(self):
        if not os.path.exists(paths.LOOPS_DIR):
            return
        wavs = [f for f in os.listdir(paths.LOOPS_DIR) if f.endswith('.wav')]
        if not wavs:
            return
        wavs.sort(key=lambda f: os.path.getmtime(os.path.join(paths.LOOPS_DIR, f)), reverse=True)
        ultimo = os.path.join(paths.LOOPS_DIR, wavs[0])
        self.ultimo_clip = AudioClip.cargar(ultimo)
        if self.on_state_change:
            self.on_state_change(f"Cargado: {self.ultimo_clip.nombre}")

    def set_clip(self, clip):
        self.ultimo_clip = clip

    def start_loop(self):
        if not self.ultimo_clip:
            if self.on_state_change:
                self.on_state_change("No hay clip")
            return

        if self.reproduciendo:
            return

        self.reproduciendo = True
        self.stop_event = threading.Event()
        if self.on_state_change:
            self.on_state_change("Reproduciendo")

        self.playback_thread = Thread(target=self._reproducir_bucle, daemon=True)
        self.playback_thread.start()

    def _reproducir_bucle(self):
        data = self.ultimo_clip.datos.astype(np.float32)
        fs = self.ultimo_clip.SAMPLE_RATE

        while self.reproduciendo and not self.stop_event.is_set():
            sd.play(data, samplerate=fs)
            # Espera hasta que termine o se pulse stop
            while not self.stop_event.is_set():
                if sd.wait() != 0:  # Terminó de reproducir
                    break
            sd.stop()

        self.reproduciendo = False
        if self.on_state_change:
            self.on_state_change("Reproducción detenida")

    def stop(self):
        if not self.reproduciendo:
            return
        self.reproduciendo = False
        if self.stop_event:
            self.stop_event.set()
        sd.stop()