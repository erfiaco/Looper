def _reproducir_en_bucle(self):
    """Hilo para bucle infinito (con wait interruptible)."""
    data = self.ultimo_clip.datos.astype(np.float32)
    fs = self.ultimo_clip.SAMPLE_RATE
    duracion = len(data) / fs  # Duración en segundos (para timeout)

    while self.reproduciendo and not self.stop_event.is_set():
        sd.play(data, fs)  # Inicia play asíncrono
        
        # ← FIX: Wait interruptible —bloquea hasta fin O hasta stop_event.set()
        self.stop_event.wait(timeout=duracion) #i thing it doesn't have to have a time out, si we say play while stop event is not pressed... it's enough. and we run it in a separate thread.
        
        sd.stop()  # Para si se interrumpió mid-play
        
        # Si el event se setó, sale del while grande
        if self.stop_event.is_set():
            break

    sd.stop()  # Limpieza final
    self.reproduciendo = False
    if self.on_state_change:
        self.on_state_change("Reproducción detenida")