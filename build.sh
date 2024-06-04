#!/bin/bash

# Install Playwright and the necessary browser binaries
pip install playwright
playwright install --with-deps chromium
