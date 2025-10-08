import sounddevice as sd
import numpy as np
from threading import Event
from software.audio_clip import AudioClip

class LooperGrabacion:
    def __init__(self, on_state_change=None):
        self.sample_rate = AudioClip.SAMPLE_RATE
        self.channels = AudioClip.CHANNELS
        self.mute = False
        self.grabando = False
        self.buffer = []
        self.stop_event = Event()
        self.on_state_change = on_state_change  # Callback para UI
        self.stream = None

    def callback_grabacion(self, indata, frames, time_info, status):
        """Callback de sounddevice."""
        if status:
            print(status)
        if self.mute:
            indata = np.zeros_like(indata)
        if self.grabando and not self.stop_event.is_set():
            self.buffer.append(indata.copy())

    def start(self):
        """Inicia grabación."""
        if self.grabando:
            return
        self.buffer = []
        self.grabando = True
        self.stop_event.clear()
        if self.on_state_change:
            self.on_state_change("Grabando")
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.callback_grabacion,
            blocksize=1024
        )
        self.stream.start()

    def stop(self):
        """Detiene y retorna clip."""
        if not self.grabando:
            return None
        self.grabando = False
        self.stop_event.set()
        if self.stream:
            self.stream.stop()
            self.stream.close()
        if self.on_state_change:
            self.on_state_change("Grabación detenida")
        if self.buffer:
            audio = np.concatenate(self.buffer)
            clip = AudioClip(audio)
            clip.guardar()
            self.buffer = []
            return clip
        return None

    def toggle_mute(self):
        """Alterna mute."""
        self.mute = not self.mute
        if self.on_state_change:
            self.on_state_change(f"Mute: {'ON' if self.mute else 'OFF'}")