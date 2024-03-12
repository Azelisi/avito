# В consumer.py
import pika
import json
from aiogram import Bot, types

# Импортируйте sender из rabbitmq.py
from rabbitmq import RabbitMQSender
from src.config.cfg import bot


def callback(body):
    message = json.loads(body)
    print(f"Received message: {message}")

    # Извлекаем текст сообщения
    text = message.get('text', '')

    # Отправляем сообщение в телеграмм
    user_id = int(body.routing_key.split('_')[1])
    bot.send_message(user_id, text)


# ...

# Добавьте обработчик для прослушивания сообщений из RabbitMQ
def listen_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='direct_logs', queue=queue_name)

    print(f' [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


# Добавьте вызов функции для прослушивания RabbitMQ в вашем основном скрипте
listen_rabbitmq()
