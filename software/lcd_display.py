# Asume tu LCD_I2C_classe está en software/ o libs/; ajusta import
import LCD_I2C_classe as LCD

class LcdDisplay:
    def __init__(self):
        self.lcd = LCD.LCD_I2C()

    def clear(self):
        self.lcd.clear()

    def write_line(self, texto, linea):
        self.lcd.write(texto, linea)

    def mostrar_estado(self, grabando, reproduciendo, mute, ultimo_clip=None):
        estado = "Grabando" if grabando else "Reproduciendo" if reproduciendo else "En espera"
        self.write_line(estado, 1)
        self.write_line(f"Mute: {'ON' if mute else 'OFF'}", 2)
        if ultimo_clip:
            self.write_line(f"Loop: {ultimo_clip.nombre}", 3)  # Asume 4 líneas; ajusta