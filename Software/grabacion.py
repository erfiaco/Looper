from libs import paths
from audio import AudioFile
import subprocess #para ejecutar el comando shell

class LooperGrabacion:
    def __init__(self):
        self.sample_rate = AudioFile.sample_rate
        self.channels = AudioFile.channels
        self.format = AudioFile.format
        self.buffer_size = AudioFile.buffer_size
        self.period_size = AudioFile.period_size
        self.grabando = False
        self.proceso = None #para manejar el proceso de grabacion
        self_on_state_change = self_on_state_change # Callback para UI

    def grabar(self):
        if self.grabando:
            return # Ya esta garbando ignora
        self.grabando = True
        arecord -D hw:1,0 -f self.format -r self.sample_rate -c self.channels --buffer-size=self.buffer_size --period-size=1024  LOOPS_DIR/prueba.wav
        if self.on_state_change:
            self.on_state_change("Grabando...")
            
    def detener_grabacion(self):
        self.grabando = False
        # Retorna un AudioFile simulado
        return AudioFile("temp.wav")  # Importa AudioFile si es necesario, pero mejor en main
