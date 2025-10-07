from . import paths
from .audio import AudioFile
import subprocess #para ejecutar el comando shell
import os



class LooperGrabacion:
    def __init__(self, on_state_change=None):
        self.sample_rate = AudioFile.sample_rate
        self.channels = AudioFile.channels
        self.format = AudioFile.format
        self.buffer_size = AudioFile.buffer_size
        self.period_size = AudioFile.period_size
        self.grabando = False #para manejar el proceso en Arecord
        self.proceso = None #para manejar el proceso de grabacion
        self.on_state_change = on_state_change # Callback para UI
        self.archivo_salida = os.path.join(paths.LOOPS_DIR, "prueba.wav")

    def grabar(self):
        if self.grabando:
            if self.on_state_change:
                self.on_state_change("Grabando...")
            return # Ya esta garbando ignora

        self.grabando = True
        if self.on_state_change:
            self.on_state_change("REC")

        cmd = [
	    'arecord',
	    '-D', 'hw:0,0', #Dispositivo alsa ajusta cn arecord -l
	    '-f', self.format,
        '-r', str(self.sample_rate),
	    '-c', str(self.channels),
        '--buffer-size', str(self.buffer_size),
	    '--period-size', str(self.period_size),
	    self.archivo_salida
        ]

        try:
            self.proceso = subprocess.Popen(cmd) #backrground, no bloquea
        except FileNotFoundError:
            if self.on_state_change:
                self.on_state_change("Error: arecord no enconttrado")
            self.grabando = False
            return

    def detener_grabacion(self):
        if not self.grabando:
            if self_on_state_change:
	            self.on_state_change("No Recording")
            return None
            
        self.grabando = False
        if self.proceso:
	        self.proceso.terminate()
	        self.proceso.wait(timeout=1)
	        try:
	            self.proceso.kill()
	        except:
		        pass
        if self.on_state_change:
	        self.on_state_change("REC Stopped")
        
	
        if os.path.exists(self.archivo_salida):
	        clip = AudioFile(self.archivo_salida)
	        return clip
        else:
	        if self.on_state_change:
		        self.on_state_change("Archivo no creado")
	        return None