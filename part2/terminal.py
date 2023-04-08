import pika
import json
import time
from flask import Flask
import threading
import queue


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

    def save_data_locally(self):
        while True:
            if not consumer.data.empty():
                data = consumer.data.get()
                with app.app_context():
                    receive_data(data)
            time.sleep(1)


app = Flask(__name__)

consumer = RabbitMQConsumer('localhost', exchange='logs')

consumer_thr = threading.Thread(target=consumer.start_consuming)
save_data_thr = threading.Thread(target=consumer.save_data_locally, args=(app,))
consumer_thr.start()
save_data_thr.start()

@app.route('/data')
def receive_data():
    data = consumer.data.get()
    # haz lo que quieras con los datos recibidos
    return 'OK, recibido dato: {}'.format(data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)



