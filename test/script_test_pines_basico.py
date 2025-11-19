# Script minimo para probar un pin
import pigpio
pi = pigpio.pi()
print("Estado GPIO26:", pi.read(26))
print("Estado GPIO6:", pi.read(6)) 
print("Estado GPIO13:", pi.read(13))
print("Estado GPIO19:", pi.read(19))
pi.stop()
