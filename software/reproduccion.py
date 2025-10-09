import sounddevice as sd
import numpy as np  # ← ¡Agregado! Para astype(float32)
from threading import Thread, Event
from software.audio_clip import AudioClip
import os
from libs import paths  # Para LOOPS_DIR

class LooperReproduccion:
    def __init__(self, ultimo_clip=None, on_state_change=None):
        self.ultimo_clip = ultimo_clip
        self.reproduciendo = False
        self.stop_event = Event()
        self.playback_thread = None
        self.on_state_change = on_state_change

        # ← NUEVO: Carga el último archivo existente si no se pasa uno
        if not self.ultimo_clip:
            self._cargar_ultimo_archivo()

    def _cargar_ultimo_archivo(self):
        """Carga el archivo .wav más reciente de LOOPS_DIR."""
        loop_dir = paths.LOOPS_DIR
        print(f"[DEBUG] Buscando en: {loop_dir}")  # ← NUEVO: ve el path
        if os.path.exists(loop_dir):
            wav_files = [f for f in os.listdir(loop_dir) if f.endswith('.wav')]
            print(f"[DEBUG] Archivos .wav encontrados: {wav_files}")  # ← NUEVO: lista
            if wav_files:
                # Ordena por fecha de mod (más reciente primero)
                wav_files.sort(key=lambda f: os.path.getmtime(os.path.join(loop_dir, f)), reverse=True)
                ultimo_path = os.path.join(loop_dir, wav_files[0])
                self.ultimo_clip = AudioClip.cargar(ultimo_path)
                if self.on_state_change:
                    self.on_state_change(f"Cargado último: {self.ultimo_clip.nombre}")
                return
        if self.on_state_change:
            self.on_state_change("No hay archivos previos para reproducir")

    def start_loop(self):
        """Inicia reproducción en bucle (carga si no hay clip)."""
        # ← NUEVO: Si no hay clip, carga el último
        if not self.ultimo_clip or not self.ultimo_clip.datos.size:
            self._cargar_ultimo_archivo()
            if not self.ultimo_clip:
                if self.on_state_change:
                    self.on_state_change("No hay clip para reproducir. Graba primero.")
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
        data = self.ultimo_clip.datos.astype(np.float32)  # ← Ahora np existe
        fs = self.ultimo_clip.SAMPLE_RATE
        while self.reproduciendo and not self.stop_event.is_set():
            sd.play(data, fs)
            sd.wait()  # Espera reproducción
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
        """Asigna nuevo clip (sobrescribe el último)."""
        self.ultimo_clip = clip