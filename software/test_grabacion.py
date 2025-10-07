from libs import paths
from libs.grabacion import LooperGrabacion  # Import local

#LooperGrabacion = grabacion.LooperGrabacion()

def main():
    grabador = LooperGrabacion()  # Sin callback para simple

    print("Iniciando grabacion... Presiona Ctrl+C para parar.")
    grabador.grabar()
    try:
        import time
        time.sleep(5)  # Graba 5 segs; cambialo por input() si quieres
    except KeyboardInterrupt:
        pass
    clip = grabador.detener_grabacion()
    if clip:
        print(f"Grabado! {clip.info()}")  # Asume que AudioFile tiene .info()

if __name__ == "__main__":
    main()
