import pika
import json
import time
import requests
import threading
import queue

class RabbitMQConsumer:
    def __init__(self, rabbitmq_host, exchange='', routing_key=''):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue, routing_key=routing_key)
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.handle_message, auto_ack=True)
        self.data = queue.Queue()
        self.url = 'http://localhost:8000/data/'

    def handle_message(self, channel, method, properties, body):
        message = json.loads(body)
        print(message)
        self.data.put(message)

    def start_consuming(self):
        print("Consumiendo datos de RabbitMQ")
        self.channel.start_consuming()

    def save_data_locally(self):
        while True:
            print("Consumiendo hilooo")
            try:
                data = self.data.get(timeout=1)
                requests.post(self.url, data=json.dumps(data))
            except queue.Empty:
                pass

consumer = RabbitMQConsumer('localhost', exchange='logs')

consumer_thr = threading.Thread(target=consumer.start_consuming)
consumer_thread = threading.Thread(target=consumer.save_data_locally)

consumer_thr.start()
consumer_thread.start()
