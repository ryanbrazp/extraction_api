"""Script para executar a aplicação."""
from api.app import app  # Não usa create_app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)