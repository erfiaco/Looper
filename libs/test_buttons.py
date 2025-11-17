#!/usr/bin/env python3
import os
import time

from gpiozero import Button
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory  # ← CORREGIDO: LGPIOFactory

# Backend oficial de Bookworm: lgpio → nunca falla
Device.pin_factory = LGPIOFactory()

print("Test de botones con pigpio")
print("Asegúrate de tener corriendo: sudo pigpiod")
print("Pulsa Ctrl+C para salir\n")

# ==== BOTONES ====
btn_grabar = Button(5)   # Rojo
btn_mute   = Button(26)    # Amarillo
btn_play   = Button(6)   # Verde
btn_stop   = Button(13, hold_time=3)  # Azul (o el que sea)

# ==== CALLBACKS ====
def grabar_pressed():
    print("BOT GRABAR PRESIONADO")

def mute_pressed():
    print("BOT MUTE PRESIONADO")

def play_pressed():
    print("BOT PLAY PRESIONADO")

def stop_pressed():
    print("BOT STOP (pulsacion corta)")

def stop_held():
    print("BOT STOP MANTENIDO 3 SEGUNDOS salieENDO")
    exit()

# ==== ASIGNAMOS EVENTOS ====
btn_grabar.when_pressed = grabar_pressed
btn_mute.when_pressed   = mute_pressed
btn_play.when_pressed   = play_pressed
btn_stop.when_pressed   = stop_pressed
btn_stop.when_held      = stop_held

print("Botones listos! Prueba pulsarlos uno a uno...\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n Chau!")
