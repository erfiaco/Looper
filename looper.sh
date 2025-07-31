#!/bin/bash

NOMBRE_ARCHIVO="grabacion_$(date +%F_%H-%M-%S).wav"
DISPOSITIVO="plughw:1,0"
FORMATO="cd"
TIEMPO_MAXIMO=10 # segundos

echo "🎙️ Grabando desde el Zoom H4n Pro..."
echo "Pulsa la barra espaciadora para detener, o espera $TIEMPO_MAXIMO segundos."
echo "Guardando en: $NOMBRE_ARCHIVO"

# Iniciar grabación
arecord -D "$DISPOSITIVO" -f "$FORMATO" -t wav "$NOMBRE_ARCHIVO" &
PID=$!

# Configurar tiempo de espera
stty -echo -icanon time 0 min 0
INICIO=$(date +%s)

while true; do
  key=$(dd bs=1 count=1 2>/dev/null)
  if [[ "$key" == " " ]]; then
    echo ""
    echo "🛑 Barra espaciadora detectada. Deteniendo grabación..."
    kill $PID
    wait $PID
    break
  fi

  AHORA=$(date +%s)
  if (( AHORA - INICIO >= TIEMPO_MAXIMO )); then
    echo ""
    echo "⏱️ Tiempo máximo alcanzado. Deteniendo grabación..."
    kill $PID
    wait $PID
    break
  fi

  sleep 0.1
done

stty sane
echo "✅ Grabación guardada en: $NOMBRE_ARCHIVO"
