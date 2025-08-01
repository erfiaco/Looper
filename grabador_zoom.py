import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy.io.wavfile as wav
import datetime
import time
from pynput import keyboard

sample_rate = 44100
channels = 2
mute = False
grabando = True
reproducir_despues = False
buffer = []

print("🎙️ Grabando desde el Zoom H4n Pro...")
print("Pulsa [barra espaciadora] o [h] para detener.")
print("Pulsa [a] para activar/desactivar mute.")

def callback(indata, frames, time, status):
    global mute
    if status:
        print(status)
    if mute:
        indata = np.zeros_like(indata)
    buffer.append(indata.copy())

def on_press(key):
    global mute, grabando, reproducir_despues

    try:
        if key.char == 'a':
            mute = not mute
            print("🎚️ Mute activado" if mute else "🔊 Mute desactivado")
        elif key.char == 'h':
            reproducir_despues = True
            grabando = False
            return False
    except AttributeError:
        if key == keyboard.Key.space:
            grabando = False
            return False

# Usamos el listener como contexto para que libere el terminal correctamente
with keyboard.Listener(on_press=on_press) as listener:
    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
        while grabando:
            sd.sleep(200)
    listener.join()  # Esperamos a que el listener termine correctamente

# Guardar archivo
audio = np.concatenate(buffer)
nombre_archivo = f"grabacion_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"
wav.write(nombre_archivo, sample_rate, audio)
print(f"✅ Grabación guardada como: {nombre_archivo}")

'''
# Reproducción
if reproducir_despues:
    print("▶️ Reproduciendo...")
    data, fs = sf.read(nombre_archivo, dtype='int16')
    sd.play(data, fs)
    sd.wait()
    print("✅ Reproducción terminada.")
'''    
    
# Reproducir el archivo recién guardado (solo si se ha grabado algo)
#if not muted and len(frames) > 0:
if reproducir_despues:
    print("▶️ Reproduciendo...")
    data, fs = sf.read(nombre_archivo, dtype='float32')
    sd.play(data, fs, device='pulse')  # ← esto fuerza salida por PulseAudio
    sd.wait()


