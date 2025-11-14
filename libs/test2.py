import pigpio
import time

pi = pigpio.pi()

pines = [26, 6, 13, 19]
nombres = {26: "GRABAR", 6: "MUTE", 13: "PLAY", 19: "STOP"}

print("Estados iniciales (deberían ser 1 = HIGH):")
for pin in pines:
    estado = pi.read(pin)
    print(f"GPIO{pin} ({nombres[pin]}): {estado} {'← NO presionado' if estado == 1 else '← PRESIONADO'}")

print("\n🎯 ¡Ahora presiona cada botón uno por uno y veremos si cambia a 0!")
print("Mantén presionado cada botón unos segundos...\n")

try:
    for i in range(20):  # Probar por 20 iteraciones
        cambios = False
        for pin in pines:
            estado = pi.read(pin)
            if estado == 0:  # Si está en LOW (presionado)
                print(f"✅ ¡BOTÓN {nombres[pin]} PRESIONADO! (GPIO{pin} = 0)")
                cambios = True
        
        if cambios:
            print("---")  # Separador cuando hay cambios
        
        time.sleep(0.5)  # Media segundo entre chequeos

except KeyboardInterrupt:
    print("\nTest terminado")

pi.stop()
