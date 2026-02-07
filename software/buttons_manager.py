from gpiozero import Button
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

class ButtonsManager:
    def __init__(self, on_grabar_press, on_mute_press, on_play_press, on_stop_press, on_long_stop):
        self.btn_grabar = Button(13, pull_up=True, bounce_time=0.03)
        self.btn_mute   = Button(19, pull_up=True, bounce_time=0.03)
        self.btn_play   = Button(6,  pull_up=True, bounce_time=0.03)
        self.btn_stop   = Button(5, pull_up=True, bounce_time=0.03, hold_time=3.0)

        # Asignacion directa

        self.btn_grabar.when_pressed = on_grabar_press
        self.btn_mute.when_pressed   = on_mute_press
        self.btn_play.when_pressed   = on_play_press
        self.btn_stop.when_pressed   = on_stop_press
        self.btn_stop.when_held      = on_long_stop

    def close(self):
        try:
            self.btn_grabar.close()
            self.btn_mute.close()
            self.btn_play.close()
            self.btn_stop.close()
        except:
            pass
