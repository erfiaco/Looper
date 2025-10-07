from libs import paths
from audio import AudioFile

class LooperReproduccion:
    def __init__(self):
        self.clips = []

    def agregar_clip(self, clip):
        self.clips.append(clip)

    def reproducir(self):
        aplay -D hw:1,0 -f  LOOPS_DIR/prueba.wav 
        print(f"Reproduciendo {len(self.clips)} clips")
