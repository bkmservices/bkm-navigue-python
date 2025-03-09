import asyncio
import logging
from flask import Flask, request, jsonify
from pyppeteer import launch

# Configurer le logging pour enregistrer les erreurs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

async def get_page_content(url):
    try:
        browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()
        
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        await page.goto(url, {"waitUntil": "networkidle2", "timeout": 30000})  # Timeout après 30s
        content = await page.content()
        await browser.close()
        return content
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction de {url}: {str(e)}")
        return None

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "Veuillez fournir une URL valide"}), 400

    try:
        content = asyncio.run(get_page_content(url))
        if content:
            return jsonify({"content": content})
        else:
            return jsonify({"error": "Impossible de récupérer le contenu"}), 500
    except Exception as e:
        logging.error(f"Erreur dans la route /scrape: {str(e)}")
        return jsonify({"error": "Une erreur interne est survenue"}), 500

if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', port=10000)
        except Exception as e:
            logging.error(f"Le serveur a rencontré une erreur: {str(e)}. Redémarrage...")
