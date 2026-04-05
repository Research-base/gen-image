import os
import time
from io import BytesIO
from PIL import Image

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images")

# Always ensure images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

def generate_filename(engine_name: str, ext: str = "png") -> str:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return os.path.join(IMAGES_DIR, f"{engine_name}_{timestamp}.{ext}")

def save_image_bytes(img_bytes: bytes, engine_name: str) -> str:
    """Save raw image bytes to file and return filepath"""
    try:
        image = Image.open(BytesIO(img_bytes))
        file_path = generate_filename(engine_name)
        image.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return ""

def save_pil_image(image: Image.Image, engine_name: str) -> str:
    """Save PIL Image to file and return filepath"""
    try:
        file_path = generate_filename(engine_name)
        image.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error saving PIL image: {e}")
        return ""
