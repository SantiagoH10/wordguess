from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"

# Pre-trained model paths
GOOGLE_MODEL_PATH = MODELS_DIR / "GoogleNews-vectors-negative300.bin"

#GloVe 6B 100d model (331MB)
GLOVE_MODEL_PATH = MODELS_DIR / "glove.6B.100d.txt"

DEFAULT_MODEL = "google" # or "glove"
