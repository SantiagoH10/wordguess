
import requests
import zipfile
from pathlib import Path
from config import MODELS_DIR, GLOVE_MODEL_PATH

def download_glove():
    # Create models directory
    MODELS_DIR.mkdir(exist_ok=True)

    # Skip if already exists
    if GLOVE_MODEL_PATH.exists():
        print(f"✅ GloVe model already exists: {GLOVE_MODEL_PATH}")
        return

    print("📥 Downloading GloVe model (331MB)...")

    # Download zip file
    url = "https://nlp.stanford.edu/data/glove.6B.zip"
    zip_path = MODELS_DIR / "glove.6B.zip"

    response = requests.get(url)
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    print("📦 Extracting...")

    # Extract only the 100d file we need
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract("glove.6B.100d.txt", MODELS_DIR)

    # Clean up zip file
    zip_path.unlink()

    print(f"✅ Done! Model saved to: {GLOVE_MODEL_PATH}")

if __name__ == "__main__":
    download_glove()
