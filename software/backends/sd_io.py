# backends/sd_io.py
# sounddevice backend: input via callback, buffer in RAM, save wav, loop playback

import os
import datetime
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile as wav

import /libs/oled_classe as oled

# state
_cfg = {
    "samplerate": 44100,
    "channels": 1,
    "blocksize": 1024,
    "device_in": None,   # e.g. "hw:0,0" or None to let PortAudio choose
    "device_out": None,  # e.g. "pulse" or "audioinjectorpi"
    "loops_dir": "loops",
    #"lcd": None,
}

_mute = False
_recording = False
_playing = False
_last_file = None
_buffer = []
_stream_in = None

def init_backend(
    samplerate=44100,
    channels=1,
    blocksize=1024,
    device_in=None,
    device_out=None,
    loops_dir="loops",
    #lcd=None,
):
    global _cfg
    _cfg.update(
        dict(
            samplerate=samplerate,
            channels=channels,
            blocksize=blocksize,
            device_in=device_in,
            device_out=device_out,
            loops_dir=loops_dir,
            #lcd=lcd,
        )
    )
    if not os.path.exists(loops_dir):
        os.makedirs(loops_dir)

def get_state():
    return {
        "mute": _mute,
        "recording": _recording,
        "playing": _playing,
        "last_file": _last_file,
    }

def is_recording():
    return _recording

def is_playing():
    return _playing

def has_buffer():
    return len(_buffer) > 0

def toggle_mute():
    global _mute
    _mute = not _mute
    return _mute

# ===== input callback =====
def _callback(indata, frames, time_info, status):
    global _buffer
    if status:
        print(status)
    if _mute:
        indata = np.zeros_like(indata)
    if _recording:
        _buffer.append(indata.copy())

# context manager for input stream
class _InputStreamCtx:
    def __enter__(self):
        global _stream_in
        _stream_in = sd.InputStream(
            samplerate=_cfg["samplerate"],
            channels=_cfg["channels"],
            callback=_callback,
            blocksize=_cfg["blocksize"],
            device=_cfg["device_in"],
            dtype="float32",
        )
        _stream_in.start()
        return _stream_in

    def __exit__(self, exc_type, exc, tb):
        global _stream_in
        try:
            if _stream_in:
                _stream_in.stop()
                _stream_in.close()
        finally:
            _stream_in = None

def input_stream():
    return _InputStreamCtx()

# ===== recording control =====
def start_recording():
    global _recording, _buffer
    _buffer = []
    _recording = True
    #_lcd_write("Grabando", 1)
    oled.oled_status("Grabando", 1)
def stop_recording():
    global _recording
    _recording = False
    #_lcd_write("Grab stop", 1)
    oled.oled_status("Stop",1)
def save_recording():
    global _buffer, _last_file
    if not _buffer:
        return None
    audio = np.concatenate(_buffer, axis=0)
    # ensure 2D array shape (frames, channels)
    if audio.ndim == 1 and _cfg["channels"] == 1:
        pass  # already 1D -> wav.write will accept if dtype is float? better convert
        audio = audio.astype(np.float32)
    # file path
    fname = f"loop_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    path = os.path.join(_cfg["loops_dir"], fname)
    # use scipy.wavfile.write (expects int16 or float32)
    wav.write(path, _cfg["samplerate"], audio)
    _last_file = path
    _buffer = []
    print(f"\nLoop saved: {os.path.basename(path)}")
    _lcd_write("Saved loop", 2)
    return path

# ===== playback loop =====
def start_loop_playback():
    global _playing
    if not _last_file or not os.path.exists(_last_file):
        return False
    data, fs = sf.read(_last_file, dtype="float32")
    _playing = True
    #_lcd_write("Play loop", 1)
    oled.oled_status("Play",1)
    # run playback in a detached thread using sd.play/sd.wait loop
    def _run():
        global _playing
        while _playing:
            sd.play(data, fs, device=_cfg["device_out"])
            sd.wait()
            if not _playing:
                sd.stop()
                break
        #_lcd_write("Play stop", 1)
        oled.oled_status("Stop",1)
    import threading
    threading.Thread(target=_run, daemon=True).start()
    return True

def stop_playback():
    global _playing
    if _playing:
        _playing = False
        sd.stop()