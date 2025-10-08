# Pruebas chorras para LooperReproduccion
# Estructura: Loop/software/test_reproducir.py
# Imports relativos asumiendo que se ejecuta desde Loop/software/

from libs import paths 
from libs.reproduccion import LooperReproduccion
from libs.audio import AudioFile
import time  # Para sleeps en tests

# Clase dummy AudioFile si no la tienes definida en otro lado
class AudioFile:
    def __init__(self, path):
        self.path = path  # Ruta al archivo WAV

class TestReproducir:
    def __init__(self):
        self.looper = LooperReproduccion()
        self.clip_path = f"{LOOPS_DIR}/prueba.wav"  # El archivo real
        self.clip1 = AudioFile(self.clip_path)
        self.clip2 = AudioFile(self.clip_path)  # Usa el mismo para simular secuencia

    def test_agregar_y_reproducir(self):
        print("=== Test: Agregar clips y reproducir secuencia ===")
        self.looper.agregar_clip(self.clip1)
        self.looper.agregar_clip(self.clip2)
        print(f"Clips agregados: {len(self.looper.clips)}")
        
        self.looper.reproducir()  # Reproduce la secuencia (prueba.wav x2)
        time.sleep(5)  # Espera un poco más para que suene (ajusta según duración del WAV)
        self.looper.pausar()
        print("Test completado.\n")

    def test_volumen(self):
        print("=== Test: Control de volumen ===")
        self.looper.set_volumen(50)  # Baja a 50%
        self.looper.agregar_clip(self.clip1)
        self.looper.reproducir()
        time.sleep(3)  # Deja sonar bajito
        self.looper.pausar()
        
        self.looper.set_volumen(100)  # Sube de nuevo
        print(f"Volumen final: {self.looper.volumen}%\n")
        print("Test completado.\n")

    def test_loop_infinito(self):
        print("=== Test: Loop infinito ===")
        self.looper.agregar_clip(self.clip1)
        self.looper.loop_infinito(0)  # Loop infinito de prueba.wav
        time.sleep(10)  # Deja loopear un rato (ajusta si es largo)
        self.looper.pausar()
        print("Test completado.\n")

    def run_all_tests(self):
        print("Iniciando tests de LooperReproduccion con prueba.wav...\n")
        self.test_agregar_y_reproducir()
        self.test_volumen()
        self.test_loop_infinito()
        print("¡Todos los tests chorras terminados! (Escucha el audio y chequea prints).")

# Ejecuta si es el main
if __name__ == "__main__":
    test = TestReproducir()
    test.run_all_tests()