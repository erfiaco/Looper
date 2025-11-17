from gpiozero import Button
from gpiozero import Device
from gpiozero.pins.native import NativeFactory
#import os
#os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

Device.pin_factory = NativeFactory()

class ButtonsManager:
    def __init__(self, on_grabar_press, on_mute_press, on_play_press, on_stop_press, on_long_stop):
        # pull_up + bounce_time = botones perfectos y sin rebotes
        self.btn_grabar = Button(26, pull_up=True, bounce_time=0.03)
        self.btn_mute   = Button(6,  pull_up=True, bounce_time=0.03)
        self.btn_play   = Button(13, pull_up=True, bounce_time=0.03)
        self.btn_stop   = Button(19, pull_up=True, bounce_time=0.03, hold_time=3.0)

        self.on_grabar_press = on_grabar_press
        self.on_mute_press   = on_mute_press
        self.on_play_press   = on_play_press
        self.on_stop_press   = on_stop_press
        self.on_long_stop   = on_long_stop

        self._setup_events()

    def _setup_events(self):
        self.btn_grabar.when_pressed = self.on_grabar_press
        self.btn_mute.when_pressed   = self.on_mute_press
        self.btn_play.when_pressed   = self.on_play_press
        self.btn_stop.when_pressed   = self.on_stop_press
        self.btn_stop.when_held      = self.on_long_stop
