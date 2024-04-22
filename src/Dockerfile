FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y wget unzip curl gnupg && \
    CHROMEDRIVER_VERSION=124.0.6367.60 && \
    mkdir -p /opt/chromedriver-${CHROMEDRIVER_VERSION} && \
    curl -sS -o /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-${CHROMEDRIVER_VERSION} && \
    #mv /opt/chromedriver-${CHROMEDRIVER_VERSION}/chromedriver_linux64/ /opt/chromedriver-${CHROMEDRIVER_VERSION} && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-${CHROMEDRIVER_VERSION}/chromedriver-linux64/chromedriver && \
    ln -fs /opt/chromedriver-${CHROMEDRIVER_VERSION}/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Установка Google Chrome
RUN curl -sS https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r config/requirements.txt 

EXPOSE 8079

CMD ["python", "parser_main.py"]
