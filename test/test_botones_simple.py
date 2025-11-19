from gpiozero import Button
import time

def probar_boton(nombre, gpio):
    boton = Button(gpio)
    
    def cuando_presionado():
        print(f"🎯 {nombre} presionado (GPIO {gpio})")
    
    boton.when_pressed = cuando_presionado
    return boton

print("🔧 PROBADOR SIMPLE DE BOTONES")
print("Presiona Ctrl+C para salir\n")

# Crear botones
botones = [
    probar_boton("GRABAR", 19),
    probar_boton("MUTE", 13),
    probar_boton("PLAY", 6),
    probar_boton("STOP", 26)
]

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n¡Prueba terminada!")
