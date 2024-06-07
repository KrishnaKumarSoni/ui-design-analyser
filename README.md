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


# Bounty for Deployment Assistance

### Objective

We are offering a Rs. 2500 bounty for successfully deploying the Web Page Analysis Tool. This tool uses Playwright and Chromium, and deploying it on platforms like GCP or Heroku has proven challenging due to the requirement for a Chrome driver in the environment.

### How to Participate
1. Deploy the application on a platform of your choice (GCP, Heroku, etc.).
2. Ensure that Chromium dependencies are correctly installed and configured in the environment.
3. Document all the steps you took to successfully deploy the application in a new file named DEPLOYMENT.md.
4. Provide screenshots or logs to demonstrate the deployment process and successful running of the application.

### Submission
1. Create a Pull Request (PR) with:
    a. Your DEPLOYMENT.md file detailing the deployment process.
    b. Any code changes required for the deployment.
2. Ensure your PR includes:
    a. Detailed step-by-step instructions.
    b. Clear documentation of any issues encountered and how they were resolved.
    c. Verification steps to demonstrate the successful deployment.

## Completeness

1. All steps from setup to deployment must be documented.
2. The documentation must include necessary configurations and modifications.
3. The process must be replicable using the provided instructions.

#### Functionality

1. The deployed application must run without errors.
2. All features of the application should function as intended.

#### Verification

1. Include steps to verify the successful deployment (e.g., accessing the deployed application, running test cases).

### Review Process
1. We will review the submitted PR within 7 days of submission.
2. If your deployment is successful and meets all criteria, we will merge your PR and award the Rs. 2500 bounty.
3. Feedback will be provided for PRs that do not meet the criteria, and resubmissions are welcome.

For any questions or further information, feel free to open an issue in the repository or contact krishna@kuberanix.com directly.

Let's make this tool accessible to everyone and revolutionize web page analysis together! 💪
