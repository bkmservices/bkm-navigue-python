import asyncio
from flask import Flask, request, jsonify
from pyppeteer import launch

app = Flask(__name__)

async def get_page_content(url):
    browser = await launch(headless=True, args=['--no-sandbox'])  # Lancer Chromium en mode headless
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})  # Attendre que la page soit entièrement chargée
    content = await page.content()  # Récupérer tout le HTML de la page
    await browser.close()
    return content

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url', 'https://www.google.com')
    content = asyncio.run(get_page_content(url))
    return jsonify({"content": content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
