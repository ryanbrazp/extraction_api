"""Inicialização do aplicativo Flask."""
import os
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
credentials_path = '/app/key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Verifica se o arquivo de credenciais existe
if not os.path.exists(credentials_path):
    logger.error(f"Arquivo de credenciais não encontrado em: {credentials_path}")
    raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {credentials_path}")
else:
    logger.info(f"Arquivo de credenciais encontrado em: {credentials_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))