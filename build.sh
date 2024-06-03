#!/bin/bash
set -e

# Create bin directory
mkdir -p bin

# Download Chrome
wget -q https://storage.googleapis.com/chrome-for-testing/125.0.6422.141/linux64/chrome-linux64.zip -O /tmp/chrome-linux64.zip
unzip /tmp/chrome-linux64.zip -d bin/
chmod +x bin/chrome

# Download ChromeDriver
wget -q https://storage.googleapis.com/chrome-for-testing/125.0.6422.141/linux64/chromedriver-linux64.zip -O /tmp/chromedriver-linux64.zip
unzip /tmp/chromedriver-linux64.zip -d bin/
chmod +x bin/chromedriver
