from gpiozero import Button
import os
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"#"rpigpio"

class ButtonsManager:
    def __init__(self, on_grabar_press, on_mute_press, on_play_press, on_stop_press, on_long_stop):
        self.btn_grabar = Button(19)
        self.btn_mute = Button(13)
        self.btn_play = Button(6)
        self.btn_stop = Button(26, hold_time=3.0)  # ← Configura hold a 3s

        self.on_grabar_press = on_grabar_press
        self.on_mute_press = on_mute_press
        self.on_play_press = on_play_press
        self.on_stop_press = on_stop_press
        self.on_long_stop = on_long_stop

        self._setup_events()

    def _setup_events(self):
        self.btn_grabar.when_pressed = self.on_grabar_press
        self.btn_mute.when_pressed = self.on_mute_press
        self.btn_play.when_pressed = self.on_play_press
        self.btn_stop.when_pressed = self.on_stop_press
        self.btn_stop.when_held = self.on_long_stop  # ← ¡Aquí! Llama callback en hold
