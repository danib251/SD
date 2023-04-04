import json
import pika
import signal

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



    def subscribe(self):
        self.channel.start_consuming()

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        print("Mensaje recibido:", data)

def sigint_handler(signal, frame):
    print('Desconectando...')
    subscriber.disconnect()
    exit(0)



subscriber = RabbitMQSubscriber('localhost', 5672)
signal.signal(signal.SIGINT, sigint_handler)

print("Conectando al broker...")

print("Suscribiendo al exchange 'logs'...")
subscriber.subscribe()

