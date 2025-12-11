#!/usr/bin/env python3
import time
import sounddevice as sd
import soundfile as sf
import numpy as np

print("=== TEST DE LATENCIA ===\n")

# Simula tu flujo: grabar → guardar → cargar → reproducir
print("1. Grabando 2 segundos...")
duration = 2
samplerate = 44100
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='float32')
sd.wait()
print("   ✓ Grabación completada")

t0 = time.time()

# Guarda (como hace tu AudioClip)
print("2. Guardando archivo...")
filename = "/tmp/test_latencia.wav"
sf.write(filename, recording, samplerate)
t1 = time.time()
print(f"   ✓ Guardado en {(t1-t0)*1000:.1f} ms")

# Carga (como hace tu reproduccion.cargar_ultimo())
print("3. Cargando archivo...")
data, sr = sf.read(filename)
t2 = time.time()
print(f"   ✓ Cargado en {(t2-t1)*1000:.1f} ms")

# Reproduce
print("4. Iniciando reproducción...")
sd.play(data, sr)
t3 = time.time()
print(f"   ✓ Reproducción iniciada en {(t3-t2)*1000:.1f} ms")

print(f"\n=== LATENCIA TOTAL: {(t3-t0)*1000:.1f} ms ===")
sd.wait()
