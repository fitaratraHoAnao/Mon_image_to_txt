import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Charger la variable d'environnement à partir du fichier .env
load_dotenv()

app = Flask(__name__)

# Charger la clé API OCR à partir de l'environnement
OCR_API_KEY = os.getenv('API_KEY_OCR')

# Fonction pour appeler l'API OCR.space avec un fichier image
def ocr_space_file(file, overlay=False, api_key=OCR_API_KEY, language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    r = requests.post('https://api.ocr.space/parse/image', files={'file': file}, data=payload)
    return r.json()

# Route pour recevoir un fichier image via POST et renvoyer uniquement le texte extrait
@app.route('/img2txt', methods=['POST'])
def img2txt():
    # Vérifier si un fichier a été envoyé
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    
    # Appeler l'API OCR.space
    ocr_result = ocr_space_file(image_file)
    
    # Extraire le texte du champ ParsedText
    try:
        parsed_text = ocr_result['ParsedResults'][0]['ParsedText']
        
        # Nettoyer le texte pour le rendre plus lisible
        cleaned_text = parsed_text.replace('\\u2022', '•').replace('\\r\\n', '\n').strip()
        
    except (KeyError, IndexError):
        return jsonify({"error": "Could not extract text from the image"}), 500
    
    # Retourner uniquement le texte extrait avec la clé 'réponse'
    return jsonify({"réponse": cleaned_text})

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
