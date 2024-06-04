# Use the official lightweight Python image.
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxdamage1 \
    libxshmfence1 \
    libasound2 \
    wget

# Install Playwright and its dependencies
RUN pip install playwright
RUN playwright install --with-deps chromium

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 to the world outside this container
EXPOSE 8080

# Run wsgi.py when the container launches
CMD ["python3", "wsgi.py"]
