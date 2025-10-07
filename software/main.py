#!/usr/bin/env python3

#ejecuta desde looper: python3 -m software.main asi lo trara como un paquete

from libs import paths
from libs import oled_clase

from audio import AudioFile
from grabacion import LooperGrabacion
from reproduccion import LooperReproduccion

def main():
    grabador = LooperGrabacion()
    reproductor = LooperReproduccion()

    # Ejemplo de uso
    grabador.grabar()
    # ... simula grabacion
    clip = grabador.detener_grabacion()
    reproductor.agregar_clip(clip)
    reproductor.reproducir()

    print(clip.info())  # Usa el metodo de AudioFile

if __name__ == "__main__":
    main()
