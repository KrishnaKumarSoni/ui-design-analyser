import os
import logging
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    url = data['url']
    try:
        screenshot_path, html_content = capture_screenshot(url)
        return jsonify({"screenshot_path": screenshot_path, "html_content": html_content})
    except Exception as e:
        logging.error(f"Error during screenshot capture: {e}")
        return jsonify({"error": str(e)}), 500

def capture_screenshot(url):
    screenshot_path = 'screenshot.png'

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.set_viewport_size({"width": 1920, "height": 1080})

        total_height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": 1920, "height": total_height})
        page.wait_for_timeout(2000)

        page.screenshot(path=screenshot_path, full_page=True)
        html_content = page.content()
        browser.close()

    logging.info(f"Screenshot captured: {screenshot_path}")
    return screenshot_path, html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
