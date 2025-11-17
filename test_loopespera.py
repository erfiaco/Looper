from gpiozero import Button
import time

# ===== CONFIGURACIÓN DE BOTONES =====
btn_grabar = Button(19)   # GPIO 19
btn_mute = Button(13)     # GPIO 13  
btn_play = Button(6)      # GPIO 6
btn_stop = Button(26)     # GPIO 26

# ===== FUNCIONES SIMPLES =====
def boton_grabar_pulsado():
    print("🎯 BOTÓN GRABAR pulsado - GPIO 19")

def boton_mute_pulsado():
    print("🎯 BOTÓN MUTE pulsado - GPIO 13")

def boton_play_pulsado():
    print("🎯 BOTÓN PLAY pulsado - GPIO 6")

def boton_stop_pulsado():
    print("🎯 BOTÓN STOP pulsado - GPIO 26")

# ===== ASIGNAR FUNCIONES =====
btn_grabar.when_pressed = boton_grabar_pulsado
btn_mute.when_pressed = boton_mute_pulsado
btn_play.when_pressed = boton_play_pulsado
btn_stop.when_pressed = boton_stop_pulsado

# ===== LOOP DE ESPERA SIMPLE =====
print("🔧 PRUEBA DE BOTONES - LOOP DE ESPERA")
print("Presiona los botones GPIO 19, 13, 6, 26")
print("Deberías ver un mensaje cada vez que pulses")
print("Presiona Ctrl+C para salir")
print("=" * 50)

try:
    contador = 0
    while True:
        # Loop simple que no bloquea
        time.sleep(0.1)
        contador += 1
        if contador % 50 == 0:  # Cada 5 segundos
            print(f"⏰ Loop activo... ({contador/10} segundos)")
            
except KeyboardInterrupt:
    print("\n👋 Prueba terminada")
