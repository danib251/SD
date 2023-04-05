import json
import pika
import signal
import matplotlib.pyplot as plt
from rich.console import Console
from flask import Flask

from multiprocessing import Process, Queue

app = Flask(__name__)

class RabbitMQSubscriber:
    def __init__(self, host, port, queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='logs', queue=self.queue_name)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.x_data = []
        self.y_data = []
        self.console = Console()
        self.values = []
        self.data = []
        self.queue = queue

    def subscribe(self):
        self.channel.start_consuming()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        print("Mensaje recibido:", data)
        self.values.append(data['air_data_mean'])
        mean = self.get_mean()
        stddev = self.get_stddev()
        self.queue.put({'mean': mean, 'stddev': stddev})

    def get_mean(self):
        if len(self.values) > 0:
            return sum(self.values) / len(self.values)
        else:
            return None

    def get_stddev(self):
        if len(self.values) > 0:
            mean = self.get_mean()
            return (sum((x - mean) ** 2 for x in self.values) / len(self.values)) ** 0.5
        else:
            return None

def sigint_handler(signal, frame):
    print('Desconectando...')
    subscriber.disconnect()
    exit(0)

@app.route('/main')
def stddev():
    while True:
        try:
            data = q.get(block=False)
            mean = data['mean']
            stddev = data['stddev']
            return 'El valor medio es {} y la desviación estándar es {}'.format(mean, stddev)
        except:
            return 'No hay suficientes datos para calcular la desviación estándar'

if __name__ == '__main__':
    q = Queue()
    subscriber = RabbitMQSubscriber('localhost', 5672, q)
    subscriber_process = Process(target=subscriber.subscribe)
    subscriber_process.start()
    app_process = Process(target=app.run)
    app_process.start()
    subscriber_process.join()
    app_process.join()
