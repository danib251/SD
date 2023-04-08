import pika
import json
import queue
import threading
from graphic import Graphic

class RabbitMQConsumer:
    def __init__(self, rabbitmq_host, exchange, routing_key=''):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue = self.result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue, routing_key=routing_key)
        
        
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.handle_message, auto_ack=True)
        self.data = queue.Queue()

    def handle_message(self, channel, method, properties, body):
        message = json.loads(body)
        print(message)
        self.data.put(message)

    def start_consuming(self):
        self.channel.start_consuming()



consumer = RabbitMQConsumer('localhost', exchange='logs')

consumer_thr = threading.Thread(target=consumer.start_consuming)

consumer_thr.start()

print("Consumer started")
graphic = Graphic(consumer.data)
graphic.process_data()




