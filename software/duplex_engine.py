import sounddevice as sd
import numpy as np
from .audio_clip import AudioClip

BLOCKSIZE = 256
FADE_SAMPLES = 1024  # ~23ms at 44100Hz — enough to hide any transition click


class DuplexEngine:
    IDLE = 'idle'
    RECORDING = 'recording'
    PLAYING = 'playing'

    def __init__(self, on_state_change=None):
        self.sample_rate = AudioClip.SAMPLE_RATE
        self.channels = AudioClip.CHANNELS
        self.on_state_change = on_state_change
        self.mute = False

        self.state = self.IDLE
        self._buffer = []
        self._loop_audio = None  # (N, channels) float32
        self._play_pos = 0
        self._last_clip = None

        self.stream = sd.Stream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback,
            blocksize=BLOCKSIZE,
            latency='low',
            dtype='float32'
        )
        self.stream.start()
        print("DuplexEngine: stream duplex iniciado")

    def _callback(self, indata, outdata, frames, time_info, status):
        state = self.state

        if state == self.RECORDING:
            data = np.zeros_like(indata) if self.mute else indata.copy()
            self._buffer.append(data)
            outdata[:] = 0

        elif state == self.PLAYING:
            loop = self._loop_audio
            if loop is None:
                outdata[:] = 0
                return
            pos = self._play_pos
            n = len(loop)
            written = 0
            while written < frames:
                chunk = min(frames - written, n - pos)
                outdata[written:written + chunk] = loop[pos:pos + chunk]
                pos = (pos + chunk) % n
                written += chunk
            self._play_pos = pos

        else:
            outdata[:] = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start_recording(self):
        if self.state == self.RECORDING:
            return
        self._buffer = []
        self._loop_audio = None
        self._play_pos = 0
        self.state = self.RECORDING
        if self.on_state_change:
            self.on_state_change('Grabando')

    def stop_recording_and_play(self):
        """Stop recording, build the loop with crossfades, and start playing immediately."""
        if self.state != self.RECORDING:
            return None

        # Flip to IDLE first so the callback stops appending while we build
        self.state = self.IDLE

        buf = self._buffer
        self._buffer = []

        if not buf:
            if self.on_state_change:
                self.on_state_change('Sin audio')
            return None

        audio = np.concatenate(buf).astype(np.float32)

        # Crossfade at loop boundaries to eliminate clicks on loop start and end
        fade_len = min(FADE_SAMPLES, len(audio) // 2)
        ramp = np.linspace(0.0, 1.0, fade_len, dtype=np.float32).reshape(-1, 1)
        audio[:fade_len] *= ramp          # fade in at start
        audio[-fade_len:] *= ramp[::-1]   # fade out at end

        clip = AudioClip(audio)
        self._last_clip = clip

        # Set loop data BEFORE flipping state so callback never sees PLAYING with None loop
        self._play_pos = 0
        self._loop_audio = audio
        self.state = self.PLAYING

        if self.on_state_change:
            self.on_state_change('Reproduciendo')

        return clip

    def stop_recording(self):
        """Stop recording without starting playback (e.g. for STOP button)."""
        if self.state != self.RECORDING:
            return None

        self.state = self.IDLE

        buf = self._buffer
        self._buffer = []

        if not buf:
            if self.on_state_change:
                self.on_state_change('Sin audio')
            return None

        audio = np.concatenate(buf).astype(np.float32)
        clip = AudioClip(audio)
        self._last_clip = clip

        if self.on_state_change:
            self.on_state_change('Grabación detenida')

        return clip

    def start_playing(self):
        """Resume playing the current loop (if one exists)."""
        if self._loop_audio is None or self.state == self.PLAYING:
            return
        self._play_pos = 0
        self.state = self.PLAYING
        if self.on_state_change:
            self.on_state_change('Reproduciendo')

    def stop_playing(self):
        if self.state != self.PLAYING:
            return
        self.state = self.IDLE
        if self.on_state_change:
            self.on_state_change('Detenido')

    def toggle_mute(self):
        self.mute = not self.mute
        if self.on_state_change:
            self.on_state_change(f"Mute {'ON' if self.mute else 'OFF'}")

    # ------------------------------------------------------------------
    # Properties for compatibility with OledDisplay
    # ------------------------------------------------------------------

    @property
    def grabando(self):
        return self.state == self.RECORDING

    @property
    def reproduciendo(self):
        return self.state == self.PLAYING

    @property
    def last_clip(self):
        return self._last_clip

    # ------------------------------------------------------------------

    def close(self):
        self.state = self.IDLE
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
        print("DuplexEngine: stream cerrado")
