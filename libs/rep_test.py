import sounddevice as sd
import soundfile as sf  # Necesita: pip install soundfile

# Cargar archivo de audio
data, samplerate = sf.read('loops/loop_20251117_182431.wav')

# Reproducir
try:
    sd.play(data, samplerate, blocking=False, loop=True)
except
    se pulsa la tecla "r", en cuyo caso haz sd.stop.
sd.wait()

# Ver información del audio
print(f"Duración: {len(data)/samplerate:.2f} segundos")
print(f"Canales: {data.shape[1] if len(data.shape) > 1 else 1}")
