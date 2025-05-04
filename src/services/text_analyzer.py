"""Funções para análise e comparação de texto."""
from unidecode import unidecode
import re
from nltk import tokenize
from src.data.lexical_filters import stopwords, base_medications

def remove_stopwords(words):
    """Remove palavras da lista de stopwords usando compreensão de lista."""
    return [word for word in words if word not in stopwords]

def compare_text(text):
    """Compara texto filtrado com medicamentos base usando similaridade de Jaccard."""
    result = ""
    tokens_text = tokenize.word_tokenize(text, language="portuguese")
    text_size = len(tokens_text)

    for medicine in base_medications:
        tokens_medicine = tokenize.word_tokenize(medicine, language="portuguese")
        medicine_size = len(tokens_medicine)
        intersection = sum(1 for token in tokens_text if token in tokens_medicine)
        union = text_size + medicine_size - intersection
        jaccard = intersection / union if union != 0 else 0

        if jaccard > 0.3:
            result = medicine

    return result

def process_text(text):
    """Pré-processa texto e compara com medicamentos."""
    if not text:
        return text, ""

    text = unidecode(text.lower())
    text = re.sub(r'[^\w\s]|\d+', '', text)
    words = text.split()
    filtered_words = remove_stopwords(words)
    filtered_text = ' '.join(filtered_words)
    matched_medication = compare_text(filtered_text)

    return text, matched_medication