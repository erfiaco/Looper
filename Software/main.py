#!/usr/bin/env python3

#ejecuta desde looper: python3 -m software.main así lo trara como un paquete

from libs import paths
from libs import oled_lsclase

from audio import AudioFile
from grabacion import LooperGrabacion
from reproduccion import LooperReproduccion

def main():
    grabador = LooperGrabacion()
    reproductor = LooperReproduccion()

    # Ejemplo de uso
    grabador.grabar()
    # ... simula grabación
    clip = grabador.detener_grabacion()
    reproductor.agregar_clip(clip)
    reproductor.reproducir()

    print(clip.info())  # Usa el método de AudioFile

if __name__ == "__main__":
    main()
