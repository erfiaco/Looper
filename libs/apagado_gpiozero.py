#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import os
import subprocess

# Mismo pin que tu boton STOP del looper
btn = Button(5, pull_up=True, hold_time=2.5)  # 2.5 segundos para no solaparse con el looper, actualmente usa el primer boton grabacion

def shutdown():
    print("BOTon STOP MANTENIDO 2.5s, APAGANDO LA RASPBERRY PI")
    # Opcional: puedes emitir un sonido, apagar LEDs, etc.
    subprocess.run(["sudo", "shutdown", "-h", "now"])

btn.when_held = shutdown

print("Servicio de apagado fisico activo (GPIO 5 - hold 2.5s)")
pause()
