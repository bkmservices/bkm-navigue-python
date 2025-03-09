import asyncio
from pyppeteer import launch
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape')
async def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Aucune URL fournie"}), 400

    try:
        browser = await launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.newPage()
        await page.goto(url, {"waitUntil": "networkidle2"})
        content = await page.content()
        await browser.close()
        return jsonify({"content": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
