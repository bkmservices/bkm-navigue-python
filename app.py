import asyncio
import json
from quart import Quart, request, jsonify
from pyppeteer import launch

app = Quart(__name__)

# Lancement unique de Pyppeteer au démarrage
browser = None

async def init_browser():
    global browser
    if browser is None:
        browser = await launch(headless=True)

async def google_search(query):
    await init_browser()  # Assure que le navigateur est lancé
    page = await browser.newPage()
    await page.goto(f"https://www.google.com/search?q={query}")

    results = await page.evaluate('''() => {
        let items = [];
        document.querySelectorAll('h3').forEach((element) => {
            let title = element.innerText;
            let link = element.parentElement.href;
            if (title && link) {
                items.push({ title, link });
            }
        });
        return items;
    }''')

    await page.close()
    return results

@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Veuillez fournir un paramètre 'q' pour la recherche."}), 400
    
    results = await google_search(query)
    return jsonify(results)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_browser())  # Lancer le navigateur avant de démarrer le serveur
    app.run(debug=True)
