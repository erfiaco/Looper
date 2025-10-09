import sounddevice as sd
import numpy as np
import time  # ← Agregado para sleep en el loop
from threading import Thread, Event
from audio_clip import AudioClip
import os
from libs import paths

class LooperReproduccion:
    # ... __init__ y otros métodos iguales

    def _reproducir_en_bucle(self):
        """Hilo para bucle infinito (con interrupción inmediata)."""
        data = self.ultimo_clip.datos.astype(np.float32)
        fs = self.ultimo_clip.SAMPLE_RATE
        duracion = len(data) / fs  # Duración en segundos (para el timer)

        while self.reproduciendo and not self.stop_event.is_set():
            sd.play(data, fs)  # Inicia play asíncrono
            
            # ← FIX: En vez de sd.wait() (bloqueante), loop con chequeo
            start_time = time.time()
            while time.time() - start_time < duracion and self.reproduciendo and not self.stop_event.is_set():
                time.sleep(0.01)  # Chequea cada 10ms (responsive, bajo CPU)
            
            sd.stop()  # Para el play actual si se interrumpió
            
            # Si se salió por event, no repite —sale del while grande
            if self.stop_event.is_set():
                break

        sd.stop()  # Limpieza final
        self.reproduciendo = False
        if self.on_state_change:
            self.on_state_change("Reproducción detenida")