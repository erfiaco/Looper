import time
from software.grabacion import LooperGrabacion
from software.reproduccion import LooperReproduccion
from software.audio_clip import AudioClip
from threading import Event

def callback_simple(mensaje):
    """Callback simple para prints (simula UI)."""
    print(f"[UI] {mensaje}")

def main():
    exit_event = Event()
    grabacion = LooperGrabacion(on_state_change=callback_simple)
    reproduccion = LooperReproduccion(on_state_change=callback_simple)
    ultimo_clip = None

    print("=== TEST LOOPER ===")
    print("Comandos: g=grabar (toggle), p=play (toggle), m=mute (toggle), q=salir")
    print("Presiona Enter después de cada comando...")

    grabando = False
    reproduciendo = False

    try:
        # Inicia stream de grabación (siempre listening, como en tu original)
        grabacion.start()  # Empieza el InputStream; callback corre

        while not exit_event.is_set():
            comando = input("\nComando: ").lower().strip()
            if comando == 'q':
                exit_event.set()
                break
            elif comando == 'g':
                if grabando:
                    ultimo_clip = grabacion.stop()
                    if ultimo_clip:
                        print(f"¡Grabado! {ultimo_clip.info()}")
                        reproduccion.set_clip(ultimo_clip)
                    grabando = False
                else:
                    grabacion.start()
                    grabando = True
            elif comando == 'p':
                if reproduciendo:
                    reproduccion.stop()
                    reproduciendo = False
                else:
                    if ultimo_clip:
                        reproduccion.start_loop()
                        reproduciendo = True
                    else:
                        print("No hay clip para reproducir. Graba primero.")
            elif comando == 'm':
                grabacion.toggle_mute()
            else:
                print("Comando inválido. Usa g, p, m o q.")

            time.sleep(0.1)  # Pequeña pausa para no spamear

    except KeyboardInterrupt:
        pass
    finally:
        print("\nLimpiando...")
        if grabando:
            ultimo_clip = grabacion.stop()
        if reproduciendo:
            reproduccion.stop()
        if ultimo_clip:
            print(f"Clip final: {ultimo_clip.info()}")
        grabacion.stream.close() if grabacion.stream else None
        print("¡Test terminado!")

if __name__ == "__main__":
    main()