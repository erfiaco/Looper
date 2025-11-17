import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy.io.wavfile as wav
import datetime
import time
import os
from gpiozero import Button
#import LCD_I2C_classe as LCD
#lcd = LCD.LCD_I2C()

# ===== CONFIGURACION =====
sample_rate = 44100
channels = 2
mute = False
grabando = False
reproducir_despues = False
reproduciendo = False
ultimo_archivo = None
buffer = []
LOOPS_DIR = "loops"

# CONFIGURACIÓN DE DISPOSITIVO DE AUDIO
input_device = 'audioinjector-pi-soundcard'
output_device = 'audioinjector-pi-soundcard'

# Crear carpeta loops si no existe
if not os.path.exists(LOOPS_DIR):
    os.makedirs(LOOPS_DIR)

# ===== BOTONES =====
btn_grabar = Button(19)   # Iniciar grabacion
btn_mute = Button(13)      # Silenciar/desmutear
btn_play = Button(6)     # Detener grabacion y reproducir desde inicio (loop)
btn_stop = Button(26)     # Detener todo

# ===== FUNCIONES =====
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    clear_screen()
    print("=== MENU GRABADORA ===")
    print("Presiona GRABAR para comenzar")
    print(f"Mute: {'ON' if mute else 'OFF'}")

def callback(indata, frames, time_info, status):
    global mute
    if status:
        print(status)
    if mute:
        indata = np.zeros_like(indata)
    buffer.append(indata.copy())

def reproducir_archivo(nombre_archivo):
    global reproduciendo
    if not os.path.exists(nombre_archivo):
        print("Archivo no encontrado")
        return
    
    print(f"\nReproduciendo {os.path.basename(nombre_archivo)} en bucle...")
    data, fs = sf.read(nombre_archivo, dtype='float32')
    
    reproduciendo = True
    while reproduciendo:
        try:
            sd.play(data, fs, device=output_device)
            sd.wait()
        except Exception as e:
            print(f"Error en reproducción: {e}")
            break

# ===== ACCIONES DE BOTONES =====
def iniciar_grabacion():
    global grabando, buffer
    if not grabando and not reproduciendo:
        print("🎙️ Iniciando grabación...")
        buffer = []  # Limpiar buffer anterior
        grabando = True
        grabar_audio()

def alternar_mute():
    global mute
    mute = not mute
    print(f"🔇 Mute: {'ACTIVADO' if mute else 'DESACTIVADO'}")

def detener_y_reproducir():
    global grabando, reproducir_despues
    if grabando:
        print("⏹️ Deteniendo grabación y reproduciendo...")
        grabando = False
        reproducir_despues = True

def detener_todo():
    global grabando, reproduciendo
    print("🛑 Deteniendo todo...")
    grabando = False
    reproduciendo = False

def grabar_audio():
    global grabando, buffer
    print("🎧 Grabando... Presiona PLAY para detener y reproducir")
    
    try:
        with sd.InputStream(samplerate=sample_rate, 
                          channels=channels, 
                          callback=callback,
                          device=input_device):
            while grabando:
                time.sleep(0.1)  # Pequeña pausa para no saturar la CPU
                
    except Exception as e:
        print(f"Error al grabar: {e}")
    
    # Guardar archivo si se grabó algo
    if buffer:
        guardar_grabacion()

def guardar_grabacion():
    global buffer, ultimo_archivo, reproducir_despues
    
    audio = np.concatenate(buffer)
    nombre_archivo = os.path.join(LOOPS_DIR, f"grabacion_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav")
    wav.write(nombre_archivo, sample_rate, audio)
    ultimo_archivo = nombre_archivo
    print(f"💾 Grabación guardada: {os.path.basename(nombre_archivo)}")
    
    # Reproducir si se solicitó
    if reproducir_despues:
        reproducir_despues = False
        reproducir_archivo(nombre_archivo)

# ===== ASIGNAR FUNCIONES A BOTONES =====
btn_grabar.when_pressed = iniciar_grabacion
btn_mute.when_pressed = alternar_mute
btn_play.when_pressed = detener_y_reproducir
btn_stop.when_pressed = detener_todo

# ===== PROGRAMA PRINCIPAL =====
mostrar_menu()
print("\nEstado: Listo - Esperando comandos...")

try:
    # Bucle principal NO BLOQUEANTE
    while True:
        # Aquí puedes agregar otras tareas si necesitas
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n👋 Programa terminado por el usuario")
    #lcd.clear()
