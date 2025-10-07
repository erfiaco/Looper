from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306  # Asumiendo SSD1306; cambia si es otra (ej. sh1106)
from luma.core.render import canvas
from PIL import ImageFont  # Para fuentes personalizadas, opcional
import time

class OledDisplay:
    def __init__(self, width=128, height=32, address=0x3C, port=1):
        """
        Inicializa la pantalla OLED.
        - width, height: Tamaño en píxeles (ej. 128x32 o 128x64).
        - address: Dirección I2C (común: 0x3C o 0x3D).
        - port: Puerto I2C (1 para Raspberry Pi rev. 2+).
        """
        serial = i2c(port=port, address=address)
        self.device = ssd1306(serial, width=width, height=height)
        self.device.clear()  # Limpia la pantalla al inicio
        self.font = ImageFont.load_default()  # Fuente por defecto; usa ImageFont.truetype para custom

    def mostrar_mensaje(self, texto, duracion=2):
        """
        Muestra un mensaje simple en la pantalla por 'duracion' segundos.
        """
        self.device.clear()
        with canvas(self.device) as draw:
            # Dibuja el texto centrado (aprox.)
            bbox = draw.textbbox((0, 0), texto, font=self.font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (self.device.width - text_width) // 2
            y = (self.device.height - text_height) // 2
            draw.text((x, y), texto, fill="white", font=self.font)
        time.sleep(duracion)  # Pausa para ver el mensaje
        self.device.clear()  # Limpia después

    def actualizar_estado(self, linea1, linea2=""):
    """
    Muestra dos líneas de texto.
    - linea1: Primera línea (obligatoria).
    - linea2: Segunda línea (opcional).
    """
    self.device.clear()
    with canvas(self.device) as draw:
        # Línea 1: arriba
        draw.text((0, 0), linea1, fill="white", font=self.font)
        
        # Línea 2: abajo (ajusta Y según tu fuente; 16 es típico para default)
        if linea2:
            draw.text((0, 16), linea2, fill="white", font=self.font)
    
    # No limpia auto, para refrescar en loop si quieres
