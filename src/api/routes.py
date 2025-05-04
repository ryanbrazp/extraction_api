"""Definição dos endpoints da API."""
from flask import Blueprint, request, jsonify
from src.services.image_processor import detect_text
from src.services.text_analyzer import process_text

api_bp = Blueprint("api", __name__)

@api_bp.route('/detect-text', methods=['POST'])
def detect_text_endpoint():
    """Endpoint para detectar texto em uma imagem enviada."""
    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    image_file = request.files['image']
    
    try:
        detected_text = detect_text(image_file)
        _, matched_medication = process_text(detected_text)
        response = {
            'matched_medication': matched_medication if matched_medication else 'Nenhum medicamento identificado'
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500