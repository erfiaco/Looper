from gpiozero import Button
import os
os.environ["GPIOZERO_PIN_FACTORY"] = "rpigpio"

class ButtonsManager:
    def __init__(self, on_grabar_press, on_mute_press, on_play_press, on_stop_press, on_long_stop):
        self.btn_grabar = Button(26)
        self.btn_mute = Button(6)
        self.btn_play = Button(13)
        self.btn_stop = Button(19)

        self.on_grabar_press = on_grabar_press
        self.on_mute_press = on_mute_press
        self.on_play_press = on_play_press
        self.on_stop_press = on_stop_press
        self.on_long_stop = on_long_stop  # Para hold 3s

        self._setup_events()

    def _setup_events(self):  
        self.btn_grabar.when_pressed = self.on_grabar_press
        self.btn_mute.when_pressed = self.on_mute_press
        self.btn_play.when_pressed = self.on_play_press
        self.btn_stop.when_pressed = self.on_stop_press  # Maneja short y long en la func

        
        # Long-press STOP (3s) to exit - ¡SIN bucle manual!
        self.btn_stop.hold_time = 3.0
        self.btn_stop.when_held = lambda: exit_event.set()

#    def check_long_press(self):
#        """Chequea hold en stop (llama desde main loop)."""
#        if self.btn_stop.is_pressed:
            # Lógica de hold aquí si quieres, o en on_stop_press
#            pass
