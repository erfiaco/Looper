#!/bin/bash

# Configura estos valores si lo deseas
DURACION=5 # Duración en segundos
NOMBRE_ARCHIVO="grabacion_$(date +%F_%H-%M-%S).wav"
DISPOSITIVO="plughw:1,0" # Asegúrate que es el Zoom H4n Pro. Cambia si hace falta.
FORMATO="cd" # CD = 44100 Hz, 16 bits, estéreo

# Mensaje informativo
echo "🎙️ Grabando $DURACION segundos desde el Zoom H4n Pro..."
echo "Guardando en: $NOMBRE_ARCHIVO"

# Ejecutar grabación
arecord -D "$DISPOSITIVO" -f "$FORMATO" -t wav -d "$DURACION" "$NOMBRE_ARCHIVO"

# Confirmación
echo "✅ Grabación completada."
