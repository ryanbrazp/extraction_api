"""Inicialização do aplicativo Flask."""
from flask import Flask
from src.api.routes import api_bp
from src.api.errors import handle_bad_request, handle_server_error
from src.config.settings import Config
import os
import json
import tempfile
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configura credenciais do Google Cloud
    logger.info("Configurando credenciais do Google Cloud...")
    logger.info(f"GOOGLE_CREDENTIALS_PATH: {Config.GOOGLE_CREDENTIALS_PATH}")
    logger.info(f"GOOGLE_CREDENTIALS_JSON exists: {bool(Config.GOOGLE_CREDENTIALS_JSON)}")

    if Config.GOOGLE_CREDENTIALS_JSON:
        try:
            # Em produção (Render), cria um arquivo temporário com o JSON
            credentials_dict = json.loads(Config.GOOGLE_CREDENTIALS_JSON)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(credentials_dict, temp_file)
                temp_file_path = temp_file.name
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path
            logger.info(f"Arquivo temporário de credenciais criado em: {temp_file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear GOOGLE_CREDENTIALS_JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao configurar credenciais: {e}")
            raise
    else:
        # Em desenvolvimento local, usa o caminho do arquivo
        if not Config.GOOGLE_CREDENTIALS_PATH or not os.path.exists(Config.GOOGLE_CREDENTIALS_PATH):
            logger.error(f"Arquivo de credenciais não encontrado: {Config.GOOGLE_CREDENTIALS_PATH}")
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {Config.GOOGLE_CREDENTIALS_PATH}")
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_CREDENTIALS_PATH
        logger.info(f"Usando arquivo de credenciais local: {Config.GOOGLE_CREDENTIALS_PATH}")

    # Registrar blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    # Manipulação de erros
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(500, handle_server_error)

    return app