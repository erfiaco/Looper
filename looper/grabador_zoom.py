
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import keyboard
import time
import os

# Configuraciones
samplerate = 44100
channels = 2
filename = f"grabacion_{time.strftime('%Y-%m-%d_%H-%M-%S')}.wav"
max_duration = 15  # segundos

print("🎙️ Grabando desde el Zoom H4n Pro...")
print("Pulsa 'a' para silenciar/activar. Pulsa 'barra espaciadora' para detener.")

recorded_data = []
muted = False
start_time = time.time()

def callback(indata, frames, time_info, status):
    global muted
    if muted:
        recorded_data.append(np.zeros_like(indata))
    else:
        recorded_data.append(indata.copy())

# Iniciar stream
with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
    while True:
        if keyboard.is_pressed("space"):
            print("\n🛑 Grabación detenida por el usuario.")
            break
        if keyboard.is_pressed("a"):
            muted = not muted
            print("\n🔇 Silencio activado." if muted else "\n🔊 Sonido activado.")
            time.sleep(0.3)  # evitar múltiples cambios con una sola pulsación
        if time.time() - start_time > max_duration:
            print("\n⏱️ Tiempo máximo alcanzado. Finalizando grabación.")
            break
        time.sleep(0.1)

# Convertir a array y guardar
audio = np.concatenate(recorded_data, axis=0)
wav.write(filename, samplerate, audio)
print(f"✅ Grabación guardada en: {filename}")
