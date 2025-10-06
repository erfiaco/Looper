class LooperReproduccion:
    def __init__(self):
        self.clips = []

    def agregar_clip(self, clip):
        self.clips.append(clip)

    def reproducir(self):
        print(f"Reproduciendo {len(self.clips)} clips")
