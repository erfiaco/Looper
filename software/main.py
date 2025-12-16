#!/usr/bin/env python3
import signal
import time
from threading import Event
from .grabacion import LooperGrabacion
from .reproduccion import LooperReproduccion
from .buttons_manager import ButtonsManager
from .oled_display import OledDisplay

class MainLooper:
    def __init__(self):
        self.exit_event = Event()

        self.display = OledDisplay()
        self.grabacion = LooperGrabacion()
        self.reproduccion = LooperReproduccion()

        # ← CALLBACKS PRIMERO
        self.grabacion.on_state_change = self._update_ui
        self.reproduccion.on_state_change = self._update_ui

        # ← ¡¡CREAMOS LOS BOTONES AL FINAL Y CON RETRASO!!
        import time
        time.sleep(1.2)   # 1,2 segundos de margen (más que suficiente)

        self.buttons = ButtonsManager(
            on_grabar_press=self._on_grabar_press,
            on_mute_press=self._on_mute_press,
            on_play_press=self._on_play_press,
            on_stop_press=self._on_stop_press,
            on_long_stop=self._on_long_stop
        )

        self.ultimo_clip = None

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.grabacion.start_listening()
        
        
    def _update_ui(self, mensaje=""):
        print(f"[UI] {mensaje}")
        # Protección: si aún no existen los objetos, solo imprime y no toca el display
        if not hasattr(self, 'display') or not hasattr(self, 'grabacion') or not hasattr(self, 'reproduccion'):
            return

        self.display.mostrar_estado(
            grabando=self.grabacion.grabando,
            reproduciendo=self.reproduccion.reproduciendo,
            mute=self.grabacion.mute,
            ultimo_clip=self.ultimo_clip
        )
        
    def _on_grabar_press(self):
        print("→ BOTÓN GRABAR pulsado")
        if self.reproduccion.reproduciendo:
            self.reproduccion.stop()
        if not self.grabacion.grabando:
            self.grabacion.start()
        else:
            self.ultimo_clip = self.grabacion.stop()
            if self.ultimo_clip:
                self.reproduccion.set_clip(self.ultimo_clip)

    def _on_mute_press(self):
        print("→ BOToN MUTE pulsado")
        self.grabacion.toggle_mute()

    def _on_play_press(self):
        import time
        print("→ BOToN PLAY pulsado")
        t0 = time.perf_counter()  # ← INICIO
        
        if self.grabacion.grabando:
            print(f"  [t] Deteniendo grabacion...")
            self.ultimo_clip = self.grabacion.stop()
            t1 = time.perf_counter()
            print(f"  [t] Grabacion detenida: {(t1-t0)*1000:.1f}ms")
            
            # ← Carga en memoria
            if self.ultimo_clip:
                self.reproduccion.set_clip(self.ultimo_clip)
                print(f"  [t] Clip cargado en memoria")            
            
            #time.sleep(0.01)
            print(f"  [t] Iniciando reproduccion...")
            self.reproduccion.start_loop()
            t2 = time.perf_counter()
            print(f"  [t] Reproducción iniciada: {(t2-t1)*1000:.1f}ms")
            print(f"  [t] LATENCIA TOTAL: {(t2-t0)*1000:.1f}ms")
            
            self._update_ui("Grabación detenida")
            
        elif self.reproduccion.reproduciendo:
            self.reproduccion.stop()
            
        else:
            # Si no está reproduciendo ni grabando → arrancamos
            self.reproduccion.start_loop()
            self._update_ui("Grabación detenida")
        

        

    def _on_stop_press(self):
        print("→ BOTÓN STOP corto")
        if self.reproduccion.reproduciendo:
            self.reproduccion.stop()
        if self.grabacion.grabando:
            self.ultimo_clip = self.grabacion.stop()
            # guarda aki:
            if self.ultimo_clip:
                self.ultimo_clip.guardar()

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
        self.reproduccion.stop()
        self.grabacion.stop_listening()
        self.display.clear()
        try:
            #from gpiozero import Device
            #Device.pin_factory.close()   # ← cierra el socket de pigpio limpiamente
            self.buttons.close()
        except:
            pass
        print("¡Adiós!")
        
        # Cuando termina, relanza el boot_menu
        import subprocess
        subprocess.Popen(["/usr/bin/python3", "/home/Javo/Proyects/boot_menu/boot_menu.py"])

        
#        import os
#        os._exit(99)

if __name__ == "__main__":
    looper = MainLooper()
    looper.run()
    
#    import os
#    os._exit(99)

