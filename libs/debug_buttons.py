#!/usr/bin/env python3
from gpiozero import Button
import os
import time

os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

print("=== DEBUG BOTONES DIRECTO ===")
print("pigpiod debe estar corriendo → sudo systemctl status pigpiod")
print("Pulsa cualquier botón, debe aparecer el mensaje INMEDIATAMENTE\n")

# Botones con pull-up y debounce
btn_grabar = Button(19, pull_up=True, bounce_time=0.03)
btn_mute   = Button(13,  pull_up=True, bounce_time=0.03)
btn_play   = Button(6, pull_up=True, bounce_time=0.03)
btn_stop   = Button(26, pull_up=True, bounce_time=0.03, hold_time=3.0)

def grabar():
    print("GRABAR PULSADO !!!")

def mute():
    print("MUTE PULSADO !!!")

def play():
    print("PLAY PULSADO !!!")

def stop_corto():
    print("STOP CORTO PULSADO !!!")

def stop_largo():
    print("STOP LARGO (3s) → SALIENDO")
    exit()

# Conexión directa (sin clases, sin wrappers, sin nada)
btn_grabar.when_pressed = grabar
btn_mute.when_pressed   = mute
btn_play.when_pressed   = play
btn_stop.when_pressed   = stop_corto
btn_stop.when_held      = stop_largo

print("Botones conectados. Pulsa lo que quieras...\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nAdiós")
