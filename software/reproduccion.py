import sounddevice as sd
import soundfile as sf
import numpy as np
import threading# import Thread
from software.audio_clip import AudioClip
from libs import paths
import os
import glob

class LooperReproduccion:
    def __init__(self, on_state_change=None):
        self.ultimo_clip = None
        self.reproduciendo = False
        self.stop_event = None
        self.playback_thread = None
        self.on_state_change = on_state_change
        #self.ultimo_archivo = self.cargar_ultimo_archivo()  # ← CORREGIDO: self. y asignar a atributo

        self.stop_event = threading.Event()
        self.reproduciendo = False
        self.thread = None


    def cargar_ultimo(self):
        # Opción 1: usando glob (más simple y legible)
        patron = os.path.join(paths.LOOPS_DIR, "*.wav")
        archivos_wav = glob.glob(patron)
    
        ultimo = max(archivos_wav, key=os.path.getmtime)  # recomiendo getmtime
        print(f"cargar_ultimo: {ultimo}")
        return ultimo
        
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
            # a continuacion Guarda el audio en memoria
        if clip:
            self.audio_en_memoria = clip.datos
            self.samplerate = clip.SAMPLE_RATE

    def start_loop(self):
        if self.reproduciendo:
            return
            
        self.reproduciendo = True
        self.stop_event.clear()  # Aseguramos que el event esté "limpio"

#        if self.on_state_change:
#            self.on_state_change("Reproduciendo loop")

        print("Reproduciendo en bucle ∞ → Pulsa STOP para detener")

        # Lanzamos la reproducción en un hilo separado
        self.thread = threading.Thread(target=self._loop_worker, daemon=True)
        self.thread.start()
#        
#        try:
#            # Cargar archivo de audio - CORREGIDO: usar self.ultimo_archivo
#            data, samplerate = sf.read(self.ultimo_archivo)
#            
#            # Reproducir
#            sd.play(data, samplerate, blocking=False, loop=True)
#            
#            if self.on_state_change:
#                self.on_state_change("Reproduciendo loop")
#            print("Reproduciendo en bucle. Presiona 'r' + Enter para detener...")
#    
#            # Esperar a que se presione 'r'
#            while self.reproduciendo:
#                key = input()  
#                if key.lower() == 'r':
#                    self.stop_loop()
#                    break
#            
#        except KeyboardInterrupt:
#            self.stop_loop()
#            print("\nReproducción interrumpida por el usuario")
#        except Exception as e:
#            print(f"Error: {e}")
#            self.reproduciendo = False
#        finally:
#            if self.on_state_change:
#                self.on_state_change("Reproducción detenida")    
#                                        

    def _loop_worker(self):
        """Reproducción desde memoria O desde disco"""
        """Este es el código que corre en segundo plano"""
        
        import time
        t_inicio_real = time.perf_counter()
        try:
            t0 = time.perf_counter()
            
            if hasattr(self, 'audio_en_memoria') and self.audio_en_memoria is not None:
                data = self.audio_en_memoria
                samplerate = self.samplerate
                print(f"Reproduciendo desde MEMORIA")
                t1 = time.perf_counter()
                print(f"  [Repro] Usar memoria: {(t1-t0)*1000:.1f}ms")
                            
            else:
                print(f"Reproduciendo desde DISCO")
                t_disco_inicio = time.perf_counter()
                archivo=self.cargar_ultimo()
                t_disco_find = time.perf_counter()
                print(f"  [Repro] Buscar archivo: {(t_disco_find - t_disco_inicio)*1000:.1f}ms")            
                
                data, samplerate = sf.read(archivo)
                
                t_disco_read = time.perf_counter()
                print(f"  [Repro] Leer WAV: {(t_disco_read - t_disco_find)*1000:.1f}ms")
                print(f"Reproduciendo desde DISCO: {archivo}")
       
                
                
            t1 = time.perf_counter()
            print(f"  Preparar audio: {(t1-t0)*1000:.1f}ms")
            
                            
            while not self.stop_event.is_set():
                # sd.play es no bloqueante con blocking=False
                sd.play(data, samplerate, loop=True)  # loop=True tiene bugs en algunas versiones
                t_play = time.perf_counter()
                print(f"  LATENCIA REAL hasta sd.play(): {(t_play - t_inicio_real)*1000:.1f}ms")
                # Esperamos a que termine la reproducción actual (o a que nos digan stop)
                while sd.get_stream().active and not self.stop_event.is_set():
                    sd.sleep(100)  # dormimos 100 ms para no saturar CPU

                # Si nos pidieron parar durante la reproducción, salimos
                if self.stop_event.is_set():
                    sd.stop()  # Forzamos parada inmediata
                    break

        except Exception as e:
            print(f"Error en reproducción: {e}")
        finally:
            sd.stop()
            self.reproduciendo = False

    def stop(self):
        if not self.reproduciendo:
            return
        self.reproduciendo = False
        if self.stop_event:
            self.stop_event.set()
        sd.stop()
