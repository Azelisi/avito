import pika
import json


class RabbitMQSender:
    def __init__(self, exchange_name='direct_logs'):
        self.sender = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    def send_message(self, routing_key, message):
        self.channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=json.dumps(message))
# Использование:
# sender = RabbitMQSender()
# sender.send_message(f'user_{user_id}', {'text': f'{new_ad_text[0]}'})
