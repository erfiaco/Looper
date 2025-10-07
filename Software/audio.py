import os

class AudioFile:
        #atributos de clase para default
        sample_rate = 44100
        channels = 2
        format = S16_LE
        buffer_size = 4069 #2048 1024
        period_size = 1024 #512 256
        grabando = False

        def __init__(self, ruta_archivo):
            #copia a instancia si necesitas
            self.sample_rate = self.sample_rate
            
            self.ubicacion = ruta_archivo
            self.nombre = os.path.basename(ruta_archivo)
            self.duracion = 5.0  # Simulado; usa soundfile.read() en real


    def info(self):
        return f"{self.nombre}: {self.duracion}s, {self.channels}ch, {self.sample_rate}Hz"
