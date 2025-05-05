"""Inicialização do aplicativo Flask."""
import os
import json
import tempfile
import logging
from flask import Flask
from api.routes import api_bp
from api.errors import handle_bad_request, handle_server_error
from api.settings import Config

# Configura logging
logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)

# Log inicial para depuração
print("DEBUG: Iniciando carregamento de app.py")
logger.info("DEBUG: Módulo app.py carregado no ambiente: %s", os.getenv('FLASK_ENV', 'unknown'))
logger.info("DEBUG: Versão do código: 2025-05-05")
logger.info("Diretório atual: %s", os.getcwd())
logger.info("Variáveis de ambiente disponíveis: %s", list(os.environ.keys()))

# Cria a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Registra blueprints e manipuladores de erro
app.register_blueprint(api_bp, url_prefix='/api')
app.register_error_handler(400, handle_bad_request)
app.register_error_handler(500, handle_server_error)

# Configura credenciais do Google Cloud
logger.info("Configurando credenciais do Google Cloud...")
logger.info(f"GOOGLE_CREDENTIALS_JSON exists: {bool(os.getenv('GOOGLE_CREDENTIALS_JSON'))}")
logger.info(f"Raw GOOGLE_CREDENTIALS_JSON: {os.getenv('GOOGLE_CREDENTIALS_JSON')[:50] if os.getenv('GOOGLE_CREDENTIALS_JSON') else 'Not set'}...")

if os.getenv('GOOGLE_CREDENTIALS_JSON'):
    try:
        logger.info("Tentando parsear GOOGLE_CREDENTIALS_JSON")
        credentials_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
        logger.info("GOOGLE_CREDENTIALS_JSON parsed successfully")
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
    logger.error("GOOGLE_CREDENTIALS_JSON não encontrado")
    raise FileNotFoundError("GOOGLE_CREDENTIALS_JSON não encontrado")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))