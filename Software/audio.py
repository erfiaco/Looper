import os

class AudioFile:
    def __init__(self, ruta_archivo):
        self.ubicacion = ruta_archivo
        self.nombre = os.path.basename(ruta_archivo)
        self.duracion = 5.0  # Simulado; usa soundfile.read() en real
        self.sample_rate = 44100
        self.channels = 2

    def info(self):
        return f"{self.nombre}: {self.duracion}s, {self.channels}ch, {self.sample_rate}Hz"
