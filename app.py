import asyncio
from flask import Flask, request, jsonify
from pyppeteer import launch

app = Flask(__name__)

async def get_page_title(url):
    browser = await launch(headless=True, args=['--no-sandbox'])  # Lancer Chromium
    page = await browser.newPage()
    await page.goto(url)
    title = await page.title()  # Récupérer le titre
    await browser.close()
    return title

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url', 'https://www.google.com')
    title = asyncio.run(get_page_title(url))
    return jsonify({"title": title})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
