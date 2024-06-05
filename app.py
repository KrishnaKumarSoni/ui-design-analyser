import re
import os
import signal
import subprocess
import logging
from flask import Flask, request, jsonify, render_template, session
from playwright.sync_api import sync_playwright
import openai
import base64
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import json


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to store progress
task_progress = 0

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate-key', methods=['POST'])
def validate_key():
    data = request.json
    api_key = data.get('api_key')
    openai.api_key = api_key
    try:
        # Making a simple API call to validate the key
        openai.models.list()
        return jsonify({"status": "valid"})
    except Exception as e:
        return jsonify({"status": "invalid", "error": str(e)}), 400

@app.route('/api/analyze', methods=['POST'])
def analyze():
    global task_progress
    task_progress = 0
    data = request.json
    url = data['url']
    api_key = data['api_key']
    logging.info(f"Received URL for analysis: {url}")

    try:
        openai.api_key = api_key
        # Capture screenshot and HTML content
        task_progress = 10
        screenshot_path, html_content = capture_screenshot(url)
        
        task_progress = 30  # Update progress after capturing the screenshot
        
        # Perform analysis
        task_progress = 50
        analysis_results = perform_analysis(screenshot_path, html_content)
        
        task_progress = 80  # Update progress after analysis completion
        
        # Convert to markdown
        task_progress = 90
        markdown_content = convert_to_markdown(analysis_results)
        
        task_progress = 100
        
        logging.info(markdown_content)

        logging.info("Analysis completed successfully")
        return jsonify({
            'analysis_results': analysis_results,
            'markdown_content': markdown_content
        })
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/progress', methods=['GET'])
def progress():
    global task_progress
    return jsonify({'progress': task_progress})

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

def encode_image(image_path):
    """
    Encodes an image to base64.
    Args:
        image_path (str): Path to the image.
    Returns:
        str: Base64 encoded image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def perform_analysis(screenshot_path, html_content):
    """
    Performs UI/UX analysis on the captured screenshot and HTML content.
    Args:
        screenshot_path (str): Path to the screenshot.
        html_content (str): HTML content of the web page.
    Returns:
        dict: Analysis results.
    """
    
    gpt4_analysis_results = analyze_content_sentiment_gpt4(html_content)

    # Extract business goal from GPT-4 analysis results
    business_goal = gpt4_analysis_results.get('business_goal', '')

    # Perform GPT-4o Vision analysis using the business goal
    gpt4o_vision_results = analyze_with_gpt4o_vision(screenshot_path, business_goal)
    
    return {
        'gpt4_analysis': gpt4_analysis_results,
        'gpt4o_vision_analysis': gpt4o_vision_results
    }

def analyze_with_gpt4o_vision(image_path, business_goal):
    """
    Uses the GPT-4o Vision API to analyze the UI/UX design of the provided image with the specified business goal.
    Args:
        image_path (str): Path to the image.
        business_goal (str): Business goal identified from content analysis.
    Returns:
        dict: Analysis results.
    """
    base64_image = encode_image(image_path)
    prompt = f"""
    Thoroughly and critically analyze this landing page image for its UI/UX design and suggest key optimizations to achieve the following business goal: {business_goal}.
    Respond just with the optimisations only please. Write nothing else. While thinking the optimizations and improvements, be highly specific and tactical. Do not respond with any generic improvements. Do not include anything outside the scope of UI/UX Design. 
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            },
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a highly critical and detail oriented ui/ux designer with 10+ years of experience and your purpose in life is to review landing pages and provide detailed critical reviews to achieve the defined business goal.",
                    }
                ]
            }

        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        logging.info("GPT-4o Vision analysis completed")
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        logging.error(f"Error in GPT-4o Vision API: {response.text}")
        return {"error": response.text}

def analyze_content_sentiment_gpt4(html_content):
    """
    Analyzes the content and sentiment of the web page using GPT-4.
    Args:
        url (str): URL of the web page.
    Returns:
        dict: GPT-4 analysis results.
    """

    logging.info('Starting content analysis')


    # Use BeautifulSoup to parse the full HTML and extract structured text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract main content using Newspaper3k
    # article = Article('')
    # article.set_html(html_content)
    # article.parse()
    # article.nlp()
    # text_content_newspaper = article.text

    # Extract additional structured text using BeautifulSoup
    text_content_soup = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])])
    # combined_text_content = text_content_soup + " " + text_content_newspaper
    combined_text_content = text_content_soup

    prompt = f"""
    Understand the content and define the business objective for the content. 
    Then, perform a sentiment analysis on this content and carefully think to suggest improvements & optimisations in the content to achieve the business goal.
    And then respond only with a JSON object containing 'business_goal' and 'content_optimizations'.

     Respond with a JSON containing the business_goal and the content_optimisations only in the following format:
    {{
      "business_goal": "<business_goal>",
      "content_optimizations": {{
            "point1": point1
            "point2": point2
            "point3": point3
            ...and so on
      }}
    }}
    
    Please don't write anything else. Be extremely detailed, tactical and thorough with your content_optimizations.

    Now the content I am going to provide you might have some issues because we are extracting this from the URL using web scraping. 
    Please ignore those and focus on defining the business goal and achieving that business goal with content optimisations. 
    Here is your content: {combined_text_content}
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are an expert content analyzer and marketer with 10+ years of experience. You are highly critical and are frustrated by the poor state of content in today's time."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        logging.info("GPT-4 content and sentiment analysis completed")
        response_text = response.json()["choices"][0]["message"]["content"].strip()
        return extract_json_from_response(response_text)
    else:
        logging.error(f"Error in GPT-4 API: {response.text}")
        return {"error": response.text}

def extract_json_from_response(response_text):
    """
    Extracts JSON data from the GPT response text.
    Args:
        response_text (str): The response text containing JSON data.
    Returns:
        dict: Parsed JSON data.
    """
    # Clean and correct the JSON format
    response_text = response_text.replace('\n', '')
    response_text = re.sub(r'\\n', '', response_text)

    # Use regex to extract the JSON response
    json_pattern = re.compile(r"\{.*\}", re.DOTALL)
    json_match = json_pattern.search(response_text)
    
    if json_match:
        json_data = json_match.group(0)
        parsed_data = json.loads(json_data)
        return parsed_data
    else:
        return {"error": "No valid JSON found"}
    

def convert_to_markdown(data):
    markdown = []
    markdown.append("# Analysis Results\n")

    # GPT-4 Analysis
    markdown.append("## Content analysis\n")
    if 'gpt4_analysis' in data:
        gpt4_data = data['gpt4_analysis']
        if isinstance(gpt4_data, dict):
            business_goal = gpt4_data.get('business_goal', 'No business goal found.')
            content_optimizations = gpt4_data.get('content_optimizations', {})
            markdown.append(f"**Business Goal:** {business_goal}\n")
            markdown.append("**Content Optimizations:**\n")
            for key, value in content_optimizations.items():
                markdown.append(f"- {value}\n")

        else:
            markdown.append(gpt4_data)

    # GPT-4o Vision Analysis
    markdown.append("## UI/UX Design Analysis\n")
    if 'gpt4o_vision_analysis' in data:
        gpt4o_vision_data = data['gpt4o_vision_analysis']
        if isinstance(gpt4o_vision_data, dict):
            for key, value in gpt4o_vision_data.items():
                markdown.append(f"**{key.replace('_', ' ').capitalize()}:** {value}\n")
        else:
            markdown.append(gpt4o_vision_data)

    return "\n".join(markdown)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)