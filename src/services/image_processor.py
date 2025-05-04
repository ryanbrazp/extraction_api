"""Funções para processamento de imagens usando Google Cloud Vision."""
from google.cloud import vision
from PIL import Image
import io
from src.config.settings import Config

client = vision.ImageAnnotatorClient()

def resize_image(image_file, max_size=Config.MAX_IMAGE_SIZE):
    """Redimensiona a imagem para reduzir o tamanho antes de enviar à API."""
    try:
        img = Image.open(image_file)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()
    except Exception as e:
        print(f"Erro ao redimensionar imagem: {e}")
        image_file.seek(0)
        return image_file.read()

def detect_text(image_file):
    """Detecta texto em uma imagem usando a API do Google Cloud Vision."""
    image_content = resize_image(image_file)
    image = vision.Image(content=image_content)

    try:
        response = client.text_detection(image=image, timeout=5.0)
    except Exception as e:
        raise Exception(f'Erro na API: {e}')

    if response.error.message:
        raise Exception(f'Erro na API: {response.error.message}')

    return response.text_annotations[0].description if response.text_annotations else ''