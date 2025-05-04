"""Inicialização do aplicativo Flask."""
from flask import Flask
from src.api.routes import api_bp
from src.api.errors import handle_bad_request, handle_server_error
from src.config.settings import Config
import os
import json
import tempfile

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configura credenciais do Google Cloud
    if Config.GOOGLE_CREDENTIALS_JSON:
        # Em produção (Render), cria um arquivo temporário com o JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(json.loads(Config.GOOGLE_CREDENTIALS_JSON), temp_file)
            temp_file_path = temp_file.name
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path
    else:
        # Em desenvolvimento local, usa o caminho do arquivo
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_CREDENTIALS_PATH

    # Registrar blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    # Manipulação de erros
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(500, handle_server_error)

    return app