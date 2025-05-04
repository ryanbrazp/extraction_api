"""Manipulação de erros da API."""
from flask import jsonify

def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400

def handle_server_error(e):
    return jsonify({"error": "Erro interno do servidor"}), 500