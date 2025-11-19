import sounddevice as sd
import numpy as np
from threading import Event
from .audio_clip import AudioClip

class LooperGrabacion:
    def __init__(self, on_state_change=None):
        self.sample_rate = AudioClip.SAMPLE_RATE
        self.channels = AudioClip.CHANNELS
        self.mute = False
        self.grabando = False
        self.buffer = []
        self.on_state_change = on_state_change
        self.stream = None
        self.stop_event = Event()
            
    def start_listening(self):
        if self.stream is not None:
            return

        # VALORES MÁGICOS QUE FUNCIONAN EN TODAS LAS PI
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.callback_grabacion,
            blocksize=256,        # ← 5.8 ms por bloque → mucho más fácil de procesar
            latency='low',        # ← mínimo retraso posible
            dtype='float32'       # ← más ligero que int16
        )
        self.stream.start()
        print("Grabación en modo listening (optimizado)")


    def callback_grabacion(self, indata: np.ndarray, frames: int, time_info, status):
        # ¡¡¡NUNCA imprimir nada aquí si no es crítico!!!
        # Un solo print() puede causar overflow
        if status:
            # Solo avisamos overflows graves (los leves los ignoramos)
            pass  # ← aquí no hacemos nada, es normal en Pi

        # Mute = silencio real
        if self.mute:
            data_to_save = np.zeros_like(indata, dtype=np.float32)
        else:
            data_to_save = indata.copy().astype(np.float32)

        # Solo guardamos si estamos grabando
        if self.grabando and not self.stop_event.is_set():
            self.buffer.append(data_to_save)
            



    def stop_listening(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def start(self):
        if self.grabando:
            return
        self.buffer = []
        self.grabando = True
        self.stop_event.clear()
        if self.on_state_change:
            self.on_state_change("Grabando")

    def stop(self):
        if not self.grabando:
            return None
        self.grabando = False
        self.stop_event.set()

        if self.buffer:
            audio = np.concatenate(self.buffer)
            clip = AudioClip(audio)
            clip.guardar()
            self.buffer = []
            if self.on_state_change:
                self.on_state_change("Grabación detenida")
            return clip
        return None

    def toggle_mute(self):
        self.mute = not self.mute
        if self.on_state_change:
            self.on_state_change(f"Mute {'ON' if self.mute else 'OFF'}")
