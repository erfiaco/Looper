from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

class OledDisplay:
    def __init__(self, port=1, address=0x3C, width=128, height=64):  # Ajusta height si es 32px
        # Inicializar I2C y device (como en tu codigo)
        self.serial = i2c(port=port, address=address)
        self.device = ssd1306(self.serial, width=width, height=height)
        self.W, self.H = self.device.size
        # Fuentes (fallback si no existe DejaVu)
        try:
            self.font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            self.font_big = ImageFont.load_default()
        self.font = ImageFont.load_default()

    def clear(self):
        """Limpia la pantalla."""
        img = Image.new("1", (self.W, self.H))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, self.W, self.H), fill=0)
        self.device.display(img)

    def mostrar_estado(self, grabando, reproduciendo, mute, ultimo_clip=None, bpm=None):
        """Dibuja estado en pantalla (adapta tu draw_status)."""
        img = Image.new("1", (self.W, self.H))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, self.W, self.H), fill=0)  # Limpia

        # Linea 1: Modo/Estado
        modo = "Grabando" if grabando else "Reproduciendo" if reproduciendo else "En espera"
        d.text((0, 0), f"Mode: {modo}", font=self.font_big, fill=255)

        # Linea 2: Mute
        mute_text = f"Mute: {'ON' if mute else 'OFF'}"
        d.text((0, 28), mute_text, font=self.font_big, fill=255)

        # Linea 3: ultimo loop (si hay)
        if ultimo_clip:
            d.text((0, 45), f"Loop: {ultimo_clip.nombre}", font=self.font, fill=255)

        # Linea 4: BPM (placeholder; omite si None)
        if bpm:
            d.text((0, 55), f"Tempo: {bpm} BPM", font=self.font, fill=255)

        # Muestra
        self.device.display(img)