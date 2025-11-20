#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import os

button = Button(5, pull_up=True, hold_time=2)  # hold_time = segundos para long press

def apagar():
    print("Apagando la Raspberry!")
    os.system("sudo shutdown -h now")

button.when_held = apagar

print("Boton de apagado activo. Manten ulsado 2s para apagar.")
pause()  # espera eternamente a eventos
