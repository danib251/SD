import json
import pika
import requests

class RabbitMQSubscriber:
    def __init__(self, host, port):
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
        self.values = []
        self.data = []

    def start_subscriber(self):
        self.channel.start_consuming()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        mean = self.get_mean()
        stddev = self.get_stddev()
        self.data.append({'mean': mean, 'stddev': stddev})

        # Enviar respuesta por HTTP
        response = requests.post('http://example.com', json=data)
        if response.status_code == 200:
            print('La respuesta fue enviada exitosamente')
        else:
            print(f'Hubo un error al enviar la respuesta: {response.status_code}')

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
        
    def get_data(self):
        return self.data
subscriber = RabbitMQSubscriber('localhost', 5672)
subscriber.start_subscriber()