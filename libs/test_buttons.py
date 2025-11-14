#!/usr/bin/env python3
from gpiozero import Button
import os
import time

# Forzamos pigpio (el mismo que usas en tu looper)
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

print("Test de botones con pigpio")
print("Asegúrate de tener corriendo: sudo pigpiod")
print("Pulsa Ctrl+C para salir\n")

# ==== BOTONES ====
btn_grabar = Button(26)   # Rojo
btn_mute   = Button(6)    # Amarillo
btn_play   = Button(13)   # Verde
btn_stop   = Button(19, hold_time=3)  # Azul (o el que sea)

# ==== CALLBACKS ====
def grabar_pressed():
    print("BOTÓN GRABAR PRESIONADO")

def mute_pressed():
    print("BOTÓN MUTE PRESIONADO")

def play_pressed():
    print("BOTÓN PLAY PRESIONADO")

def stop_pressed():
    print("BOTÓN STOP (pulsación corta)")

def stop_held():
    print("BOTÓN STOP MANTENIDO 3 SEGUNDOS → SALIENDO")
    exit()

# ==== ASIGNAMOS EVENTOS ====
btn_grabar.when_pressed = grabar_pressed
btn_mute.when_pressed   = mute_pressed
btn_play.when_pressed   = play_pressed
btn_stop.when_pressed   = stop_pressed
btn_stop.when_held      = stop_held

print("¡Botones listos! Prueba pulsarlos uno a uno...\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n¡Chau!")
