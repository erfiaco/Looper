import os

LOOPS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "loops")

def get_loop_path(nombre):
    """Genera path completo para un loop."""
    if not os.path.exists(LOOPS_DIR):
        os.makedirs(LOOPS_DIR)
    return os.path.join(LOOPS_DIR, nombre)