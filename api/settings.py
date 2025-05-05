"""Configurações do projeto."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    MAX_IMAGE_SIZE = (1024, 1024)