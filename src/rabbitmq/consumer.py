import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='direct_logs', queue=queue_name)

print(f' [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C')


def callback(body):
    message = json.loads(body)
    print(f"Received message: {message}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
