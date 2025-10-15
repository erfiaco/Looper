import signal
import time
import os
from threading import Event, Thread
from grabacion import LooperGrabacion
from reproduccion import LooperReproduccion
from buttons_manager import ButtonsManager
from oled_display import OledDisplay  # ← Cambio: nuevo import
from audio_clip import AudioClip

class MainLooper:
    def __init__(self):
        self.exit_event = Event()
        self.grabacion = LooperGrabacion(on_state_change=self._update_ui)
        self.reproduccion = LooperReproduccion(on_state_change=self._update_ui)
        self.display = OledDisplay()  # ← Inicializa OLED (ajusta params si necesitas)
        self.buttons = ButtonsManager(
            self._on_grabar_press,
            self._on_mute_press,
            self._on_play_press,
            self._on_stop_press, 
            self._on_longstop_press
        )
        self.ultimo_clip = None
        self.monitor_thread = None

        # Signals
        signal.signal(signal.SIGINT, self._handler_senal)
        signal.signal(signal.SIGTERM, self._handler_senal)

    def _update_ui(self, mensaje):
        """Callback unificado: parsea mensaje y actualiza OLED."""
        print(mensaje)  # Para consola
        # Actualiza OLED con estados actuales (simple parseo; mejora si quieres)
        if "Mute" in mensaje:
            self.display.mostrar_estado(
                self.grabacion.grabando, self.reproduccion.reproduciendo,
                self.grabacion.mute, self.ultimo_clip
            )
        elif "Grabando" in mensaje or "Reproduciendo" in mensaje or "detenida" in mensaje:
            self.display.mostrar_estado(
                self.grabacion.grabando, self.reproduccion.reproduciendo,
                self.grabacion.mute, self.ultimo_clip
            )

    def _on_longstop_press(self):
        if self.reproduccion.reproduciendo:
            self.reproduccion.stop()
            print("longpressed stop")

        if self.grabacion.grabando:
            self.grabacion.stop()
            print("Deb. long prrds stop")

        else 
            return: self.exitevent.set()
            print("apagando dispositivo")
            time.sleep(2)
    
    def _on_grabar_press(self):
        """Callback botón grabar."""
        if self.reproduccion.reproduciendo:
            self.reproduccion.stop()
        if not self.grabacion.grabando:
            self.grabacion.start()
        else:
            self.ultimo_clip = self.grabacion.stop()
            if self.ultimo_clip:
                self.reproduccion.set_clip(self.ultimo_clip)

    def _on_mute_press(self):
        self.grabacion.toggle_mute()

    def _on_play_press(self):
        """Callback botón play."""
        if self.grabacion.grabando:
            self.ultimo_clip = self.grabacion.stop()
            if self.ultimo_clip:
                self.reproduccion.set_clip(self.ultimo_clip)
                self.reproduccion.start_loop()
        elif self.ultimo_clip:
            if self.reproduccion.reproduciendo:
                self.reproduccion.stop()
            else:
                self.reproduccion.start_loop()

    def _on_stop_press(self):
        """Callback botón stop (short: stop, long: exit)."""
        if self.reproduccion.reproduciendo:
            self.reproduccion.stop()
        if self.grabacion.grabando:
            self.ultimo_clip = self.grabacion.stop()
        # Para long press: usa un timer en un hilo si quieres, pero por ahora short

    def _handler_senal(self, signum, frame):
        self.exit_event.set()



    def _monitorear_salida(self):
        """Hilo para chequeo de long press en stop (3s)."""
        while not self.exit_event.is_set():
            if self.buttons.btn_stop.is_pressed:
                inicio = time.time()
                while self.buttons.btn_stop.is_pressed and (time.time() - inicio < 3):
                    time.sleep(0.1)
                if time.time() - inicio >= 3:
                    self.exit_event.set()
            time.sleep(0.1)

    def run(self):
        """Loop principal."""
        self.display.mostrar_estado(  # Inicial
            self.grabacion.grabando, self.reproduccion.reproduciendo,
            self.grabacion.mute, self.ultimo_clip
        )
        self.monitor_thread = Thread(target=self._monitorear_salida, daemon=False)
        self.monitor_thread.start()

        try:
            # Inicia el stream de grabación (siempre listening)
            with self.grabacion.stream:  # Asume que en LooperGrabacion agregas self.stream en init/start
                while not self.exit_event.is_set():
                    time.sleep(0.1)
                    # Actualiza display cada 0.5s o en callbacks
                    if time.time() % 0.5 < 0.1:  # Opcional: refresh periódico
                        self.display.mostrar_estado(
                            self.grabacion.grabando, self.reproduccion.reproduciendo,
                            self.grabacion.mute, self.ultimo_clip
                        )
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        print("Limpiando...")
        self.display.clear()  # ← Limpia OLED al final
        self.grabacion.stop()
        self.reproduccion.stop()
        if self.grabacion.buffer:  # Si buffer pendiente
            self.ultimo_clip = self.grabacion.stop()
        print("Programa terminado")

if __name__ == "__main__":
    looper = MainLooper()
    looper.run()
