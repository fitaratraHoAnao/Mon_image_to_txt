import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Charger la variable d'environnement à partir du fichier .env
load_dotenv()

app = Flask(__name__)

# Charger la clé API OCR à partir de l'environnement
OCR_API_KEY = os.getenv('API_KEY_OCR')

# Fonction pour appeler l'API OCR.space via URL
def ocr_space_url(url, overlay=False, api_key=OCR_API_KEY, language='eng'):
    payload = {
        'url': url,
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    r = requests.post('https://api.ocr.space/parse/image', data=payload)
    return r.json()

# Route pour recevoir une URL d'image et renvoyer le texte extrait
@app.route('/img2txt', methods=['POST'])
def img2txt():
    data = request.get_json()
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400
    
    # Appeler l'API OCR.space
    ocr_result = ocr_space_url(url=image_url)
    
    # Retourner la réponse de l'OCR
    return jsonify(ocr_result)

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
