from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Inicializar comunicacion i2c y pantalla
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Dimensiones de la pantalla
W, H = device.size

# Fuente por defecto
font = ImageFont.load_default()
font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

def draw_status(mode, bpm):
    # Crear nueva imagen en modo 1-bit
    img = Image.new("1", (W, H))
    d = ImageDraw.Draw(img)

    # Limpiar pantalla
    d.rectangle((0, 0, W, H), fill=0)

    # Dibujar texto
    d.text((0, 0), f"Mode: {mode}", font=font_big, fill=255)
    d.text((0, 28), f"Tempo: {bpm} BPM", font=font_big, fill=255)

    # Mostrar en pantalla
    device.display(img)


# Variables iniciales
#mode, bpm = "REC", 120

# Bucle principal
#while True:
#    draw_status(mode, bpm)
#    time.sleep(0.25)

#EN EL FILE QUE USARA ESTA CLASE ESCRIBO:
#import oled_clase as oled
#import time


#mode = "REC"
#bpm = 120

#while True:
#    oled.draw_status(mode, bpm)
#    time.sleep(0.25)
