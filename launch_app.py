import subprocess
import sys
import os
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    # Get the path to the current Python interpreter
    python_interpreter = sys.executable

    # Start the Flask app
    subprocess.Popen([python_interpreter, "app.py"])
    
    # Open the web browser after a short delay
    Timer(1, open_browser).start()
