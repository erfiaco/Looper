#!/usr/bin/env python3
import signal
import time
from threading import Event
from .duplex_engine import DuplexEngine
from .buttons_manager import ButtonsManager
from .oled_display import OledDisplay


class MainLooper:
    def __init__(self):
        self.exit_event = Event()
        self.necesita_guardarse = False

        self.display = OledDisplay()
        self.engine = DuplexEngine(on_state_change=self._update_ui)

        time.sleep(1.2)

        self.buttons = ButtonsManager(
            on_btn_1_press=self._on_btn_1_press,
            on_btn_2_press=self._on_btn_2_press,
            on_btn_2_hold=self._on_btn_2_hold,
            on_btn_3_press=self._on_btn_3_press,
            on_btn_4_press=self._on_btn_4_press,
            on_long_stop=self._on_long_stop
        )

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _update_ui(self, mensaje=""):
        print(f"[UI] {mensaje}")
        if not hasattr(self, 'display') or not hasattr(self, 'engine'):
            return
        self.display.mostrar_estado(
            grabando=self.engine.grabando,
            reproduciendo=self.engine.reproduciendo,
            mute=self.engine.mute,
            ultimo_clip=self.engine.last_clip
        )

    def _on_btn_1_press(self):
        if self.engine.reproduciendo:
            return  # future: overdub
        if not self.engine.grabando:
            self.engine.start_recording()
        else:
            clip = self.engine.stop_recording_and_play()
            if clip:
                self.necesita_guardarse = True
        self._update_ui()

    def _on_btn_2_press(self):
        if self.engine.grabando:
            self.engine.stop_recording()
        elif self.engine.reproduciendo:
            self.engine.stop_playing()
        elif self.engine.has_loop:
            self.engine.start_playing()
        self._update_ui()

    def _on_btn_2_hold(self):
        self.engine.clear_loop()
        self.necesita_guardarse = False
        self._update_ui()

    def _on_btn_3_press(self):
        self.engine.toggle_mute()

    def _on_btn_4_press(self):
        if self.engine.reproduciendo:
            self.engine.stop_playing()
            if self.necesita_guardarse and self.engine.last_clip:
                print("  Guardando loop a disco...")
                self.engine.last_clip.guardar()
                self.necesita_guardarse = False

        if self.engine.grabando:
            clip = self.engine.stop_recording()
            if clip:
                clip.guardar()
                self.necesita_guardarse = False
        self._update_ui()

    def _on_long_stop(self):
        print("Long press detectado → Saliendo...")
        self.exit_event.set()

    def _signal_handler(self, signum, frame):
        print("\nSeñal recibida → Saliendo limpiamente")
        self.exit_event.set()

    def run(self):
        self._update_ui("Ready")
        try:
            while not self.exit_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        print("Limpiando recursos...")
        self.engine.close()
        time.sleep(0.3)
        self.display.clear()
        try:
            self.buttons.close()
        except Exception:
            pass
        print("¡Adiós!")
        import subprocess
        subprocess.Popen(["/usr/bin/python3", "/home/Javo/Proyects/boot_menu/boot_menu.py"])


if __name__ == "__main__":
    looper = MainLooper()
    looper.run()
