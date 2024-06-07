# ui-design-analyser

# Web Page Analysis Tool

This project is a Flask-based web application for analyzing web pages. It captures screenshots, extracts HTML content, and performs content and UI/UX analysis using OpenAI's GPT-4o API.

## Features

- **Web Page Analysis**: Capture screenshots and HTML content of web pages.
- **Content Analysis**: Perform content analysis using OpenAI's GPT-4o API.
- **UI/UX Design Analysis**: Analyze UI/UX design using OpenAI's GPT-4o Vision API.
- **Progress Tracking**: Track the progress of the analysis task.
- **Markdown Conversion**: Convert analysis results to Markdown format.

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/web-page-analysis-tool.git
   cd web-page-analysis-tool
   ```
2. **Install Requirements**

    ```sh
    pip install -r requirements.txt
    playwright install
    ```
3. **Start the Flask Application**

    ```
    python app.py
    ```

4. **Access the Application**

    Open your web browser and navigate to http://localhost:5000 to access the application.

5. **Analyze a Web Page**

    a. Enter the URL of the web page you want to analyze.
    b. Provide your OpenAI API key if prompted.
    c. Click on the analyze button to start the analysis.

    The analysis results will be displayed and available for download in Markdown format.

6. **Project Structure**
    web-page-analysis-tool/
    ├── app.py                  # Main application file
    ├── requirements.txt        # Python dependencies
    ├── templates/
    │   └── index.html          # HTML template for the main page
    └── .env.example            # Example environment file

6. **Contributing**
    Contributions are welcome! Please feel free to submit a Pull Request.