from libs import paths
from audio import AudioFile

class LooperGrabacion:
    def __init__(self, sample_rate=44100, channels=2):
        self.sample_rate = AudioFile.sample_rate
        self.channels = AudioFile.channels
        self.format = S16_LE
        self.buffer_size = 4069 #2048
        self.period_size = 1024 #512
        self.grabando = False

    def grabar(self):
        self.grabando = True
        arecord -D hw:1,0 -f self.format -r self.sample_rate -c self.channels --buffer-size=self.buffer_size --period-size=1024  LOOPS_DIR/prueba.txt

    def detener_grabacion(self):
        self.grabando = False
        # Retorna un AudioFile simulado
        return AudioFile("temp.wav")  # Importa AudioFile si es necesario, pero mejor en main
