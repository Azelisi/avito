FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r config/requirements.txt

RUN apt-get update && apt-get install -y wget unzip curl gnupg && \
    CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    mkdir -p /opt/chromedriver-${CHROMEDRIVER_VERSION} && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-${CHROMEDRIVER_VERSION} && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-${CHROMEDRIVER_VERSION}/chromedriver && \
    ln -fs /opt/chromedriver-${CHROMEDRIVER_VERSION}/chromedriver /usr/local/bin/chromedriver

# Установка Google Chrome
RUN curl -sS https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8079

CMD ["python", "parser_main.py"]
