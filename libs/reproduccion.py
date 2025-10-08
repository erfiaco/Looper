import subprocess
import threading
from .audio import AudioFile
from . import paths

class LooperReproduccion:
    def __init__(self):
        self.clips = []  # Lista de AudioFile
        self.posicion = 0.0
        self.reproduciendo = False
        self.proceso_actual = None  # Para terminar la reproduccion en curso

    def agregar_clip(self, clip: AudioFile):
        self.clips.append(clip)

    def reproducir(self):
        if not self.clips:
            print("No hay clips para reproducir.")
            return
        self.reproduciendo = True
        print(f"Reproduciendo {len(self.clips)} clips desde {self.posicion}s")
        # Iniciar en un hilo para no bloquear
        thread = threading.Thread(target=self._reproducir_secuencia)
        thread.start()

    def _reproducir_secuencia(self):
        try:
            for clip in self.clips:
                if not self.reproduciendo:
                    break
                self.proceso_actual = subprocess.Popen(['aplay', clip.path])
                self.proceso_actual.wait()  # Espera a que termine este clip
                if self.proceso_actual.returncode != 0:
                    print(f"Error al reproducir {clip.path}")
                self.proceso_actual = None
                # Aqui podrias actualizar self.posicion += clip.duracion si AudioFile lo tiene
        finally:
            self.reproduciendo = False

    def pausar(self):
        self.reproduciendo = False
        if self.proceso_actual:
            self.proceso_actual.terminate()
            self.proceso_actual.wait()  # Espera a que termine
            print("Reproduccion pausada y proceso terminado.")
            self.proceso_actual = None

    def loop_infinito(self, clip_index=0):
        if clip_index >= len(self.clips):
            print("indice de clip invalido.")
            return
        self.reproduciendo = True
        print(f"Iniciando loop infinito del clip {clip_index}")
        # Iniciar en un hilo para no bloquear
        thread = threading.Thread(target=self._loop_clip, args=(clip_index,))
        thread.start()

    def _loop_clip(self, clip_index):
        clip = self.clips[clip_index]
        try:
            while self.reproduciendo:
                self.proceso_actual = subprocess.Popen(['aplay', clip.path])
                self.proceso_actual.wait()  # Reproduce y espera
                if self.proceso_actual.returncode != 0:
                    print(f"Error en el loop del clip {clip.path}")
                    break
                self.proceso_actual = None
                self.posicion = 0  # Reinicia posicion
        finally:
            self.reproduciendo = False
