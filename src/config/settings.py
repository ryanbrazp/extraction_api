"""Configurações do projeto."""
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Carrega o caminho do arquivo de credenciais para desenvolvimento local
    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # Carrega o conteúdo JSON das credenciais para produção
    GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    MAX_IMAGE_SIZE = (1024, 1024)