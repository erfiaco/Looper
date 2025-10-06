import os

# raiz del proyecto (un nivel arriba de /libs)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# carpetas utiles
LIBS_DIR = os.path.join(BASE_DIR, "libs")
SOFTWARE_DIR = os.path.join(BASE_DIR, "Software")
LOOPS_DIR = os.path.join(BASE_DIR, "loops")

# asegurate de que loops exista
os.makedirs(LOOPS_DIR, exist_ok=True)
