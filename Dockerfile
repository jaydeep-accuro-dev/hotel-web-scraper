# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libglib2.0-0 \
    libnspr4 \
    libx11-6 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    wget \
    libasound2

# Download and install Google Chrome
RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip
RUN unzip /tmp/chrome-linux64.zip -d /opt/
RUN ln -s /opt/chrome-linux64/chrome /usr/bin/google-chrome
RUN rm /tmp/chrome-linux64.zip

# Download and install ChromeDriver
RUN wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin/
RUN rm /tmp/chromedriver-linux64.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application source code
COPY src /app/src

# Command to run your script
CMD ["python", "src/destinations/Auburn_Alabama_United_States.py"]