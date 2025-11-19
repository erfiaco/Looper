import sounddevice as sd
import soundfile as sf  # Necesita: pip install soundfile


import os

def cargar_ultimo_audio(carpeta="loops"):
    """Carga el archivo con nombre más reciente"""
    archivos = os.listdir(carpeta)
    
    # Filtrar solo .wav y encontrar el nombre MAYOR (más reciente)
    archivos_wav = [f for f in archivos if f.endswith('.wav')]
    
    if not archivos_wav:
        raise FileNotFoundError(f"No hay archivos WAV en {carpeta}")
    
    archivo_mas_reciente = max(archivos_wav)  # ¡Esto funciona porque los nombres son fechas!
    ruta_completa = os.path.join(carpeta, archivo_mas_reciente)
    
    return ruta_completa

# USO
ultimo_archivo = cargar_ultimo_audio("loops")
print(f"Último archivo: {ultimo_archivo}")




# Cargar archivo de audio
data, samplerate = sf.read(ultimo_archivo)

# Reproducir
try:
    sd.play(data, samplerate, blocking=False, loop=True)
    print("Reproduciendo en bucle. Presiona 'r' para detener...")
    
    # Esperar a que se presione 'r'
    while True:
        key = input()  # Espera entrada del usuario
        if key.lower() == 'r':
            sd.stop()
            print("Reproducción detenida")
            break
            
except KeyboardInterrupt:
    sd.stop()
    print("\nReproducción interrumpida por el usuario")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Asegurarse de que se detiene
    sd.stop()

# Ver información del audio
print(f"Duración: {len(data)/samplerate:.2f} segundos")
print(f"Canales: {data.shape[1] if len(data.shape) > 1 else 1}")
