import sounddevice as sd
import soundfile as sf
import numpy as np
from threading import Thread
from software.audio_clip import AudioClip
from libs import paths
import os

class LooperReproduccion:
    def __init__(self, on_state_change=None):
        self.ultimo_clip = None
        self.reproduciendo = False
        self.stop_event = None
        self.playback_thread = None
        self.on_state_change = on_state_change
        self.ultimo_archivo = self.cargar_ultimo_archivo()  # ← CORREGIDO: self. y asignar a atributo

    def cargar_ultimo_archivo(self, carpeta="loops"):  # ← CORREGIDO: falta self
        """Carga el archivo con nombre más reciente"""
        archivos = os.listdir(carpeta)
    
        # Filtrar solo .wav y encontrar el nombre MAYOR (más reciente)
        archivos_wav = [f for f in archivos if f.endswith('.wav')]
    
        if not archivos_wav:
            raise FileNotFoundError(f"No hay archivos WAV en {carpeta}")
    
        archivo_mas_reciente = max(archivos_wav)
        ruta_completa = os.path.join(carpeta, archivo_mas_reciente)
        print(f"Último archivo cargado: {archivo_mas_reciente}")
    
        return ruta_completa

    def set_clip(self, clip):
        self.ultimo_clip = clip

    def start_loop(self):
        if self.reproduciendo:
            return
            
        self.reproduciendo = True
        
        try:
            # Cargar archivo de audio - CORREGIDO: usar self.ultimo_archivo
            data, samplerate = sf.read(self.ultimo_archivo)
            
            # Reproducir
            sd.play(data, samplerate, blocking=False, loop=True)
            
            if self.on_state_change:
                self.on_state_change("Reproduciendo loop")
            print("Reproduciendo en bucle. Presiona 'r' + Enter para detener...")
    
            # Esperar a que se presione 'r'
            while self.reproduciendo:
                key = input()  
                if key.lower() == 'r':
                    self.stop_loop()
                    break
            
        except KeyboardInterrupt:
            self.stop_loop()
            print("\nReproducción interrumpida por el usuario")
        except Exception as e:
            print(f"Error: {e}")
            self.reproduciendo = False
        finally:
            if self.on_state_change:
                self.on_state_change("Reproducción detenida")    
                                        
    def stop(self):
        if not self.reproduciendo:
            return
        self.reproduciendo = False
        if self.stop_event:
            self.stop_event.set()
        sd.stop()
