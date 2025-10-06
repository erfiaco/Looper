class LooperGrabacion:
    def __init__(self, sample_rate=44100, channels=2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.grabando = False

    def grabar(self):
        self.grabando = True
        print("Grabando...")

    def detener_grabacion(self):
        self.grabando = False
        # Retorna un AudioFile simulado
        return AudioFile("temp.wav")  # Importa AudioFile si es necesario, pero mejor en main
