import json
import pika
import signal
import matplotlib.pyplot as plt
from rich.console import Console

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
        self.x_data = []
        self.y_data = []
        self.console = Console()
        self.values = []
        self.data = [] # Agrega esta línea
        


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
        response = app.response_class(
            response='El valor medio es {} y la desviación estándar es {}'.format(mean, stddev),
            status=200,
            mimetype='text/plain'
        )   

        # Asignar la respuesta HTTP a la vista correspondiente
        app.view_functions['mean'] = response

        '''self.x_data.append(data["air_data_mean"])
        self.y_data.append(data["co2_data_mean"])
        print("Generando gráfica...")
        plt.plot(subscriber.x_data, subscriber.y_data)
        plt.show()
        ------------------------------------------------------------------------------------------------
        self.console.print("[green]Mensaje recibido:[/green]")
        with self.console.status("[bold green]Procesando datos...[/bold green]"):
            self.console.print(f"Valor de X: [bold]{data['air_data_mean']}[/bold]")
            self.console.print(f"Valor de Y: [bold]{data['co2_data_mean']}[/bold]")
        self.values.append(data['air_data_mean'])'''
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



subscriber = RabbitMQSubscriber('localhost', 5672)
#signal.signal(signal.SIGINT, sigint_handler)

from flask import Flask

app = Flask(__name__)

@app.route('/mean')
def mean():
    return 'El valor medio es 10'

@app.route('/stddev')
def stddev():
    return 'La desviación estándar es 2'

@app.route('/')
def index():
    return "Valor medio: {:.2f}\nDesviación estándar: {:.2f}".format(subscriber.get_mean(), subscriber.get_stddev())



if __name__ == '__main__':
    app.run(threaded=True)
    subscriber = RabbitMQSubscriber('localhost', 5672)
    subscriber.subscribe()
    
  
  



