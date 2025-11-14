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

    def callback_grabacion(self, indata, frames, time_info, status):
        if status:
            print("Status:", status)
        if self.mute:
            indata = np.zeros_like(indata)
        if self.grabando and not self.stop_event.is_set():
            self.buffer.append(indata.copy())

    def start_listening(self):
        """Inicia el stream siempre activo (solo listening)"""
        if self.stream is not None:
            return
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self.callback_grabacion,
            blocksize=0,
            latency='low'
        )
        self.stream.start()
        print("Grabación en modo listening")

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