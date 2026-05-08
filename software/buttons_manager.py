from gpiozero import Button
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

class ButtonsManager:
    def __init__(self, on_btn_1_press, on_btn_2_press, on_btn_2_hold, on_btn_3_press, on_btn_4_press, on_long_stop):
        self.btn_1 = Button(6,  pull_up=True, bounce_time=0.03)
        self.btn_2 = Button(26, pull_up=True, bounce_time=0.03, hold_time=2.0)
        self.btn_3 = Button(13, pull_up=True, bounce_time=0.03)
        self.btn_4 = Button(5,  pull_up=True, bounce_time=0.03, hold_time=3.0)

        # Asignacion directa

        self.btn_1.when_pressed = on_btn_1_press
        self.btn_2.when_pressed = on_btn_2_press
        self.btn_2.when_held    = on_btn_2_hold
        self.btn_3.when_pressed = on_btn_3_press
        self.btn_4.when_pressed = on_btn_4_press
        self.btn_4.when_held    = on_long_stop


    def close(self):
        try:
            self.btn_1.close()
            self.btn_2.close()
            self.btn_3.close()
            self.btn_4.close()
        except Exception as e:
            print(f"  ⚠️ Error cerrando botones: {e}")
