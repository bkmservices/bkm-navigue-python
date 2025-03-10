import asyncio
import json
from flask import Flask, request, jsonify
from pyppeteer import launch

app = Flask(__name__)

async def google_search(query):
    browser = await launch(headless=True)
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

    await browser.close()
    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Veuillez fournir un paramètre 'q' pour la recherche."}), 400
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(google_search(query))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
