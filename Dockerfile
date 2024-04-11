# Используем базовый образ Python
FROM python:3.11.5

# Устанавливаем переменную окружения для Python, чтобы выводить сообщения сразу на консоль без буферизации
ENV PYTHONUNBUFFERED=1

# Устанавливаем pip
# RUN apt-get update && apt-get install -y python3-pip

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . /app/

EXPOSE 8080

# Запускаем оба файла в контейнере
CMD ["python", "manager.py"]
