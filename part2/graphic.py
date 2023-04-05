from flask import Flask
from terminal import RabbitMQSubscriber

app = Flask(__name__)

subscriber = RabbitMQSubscriber('localhost', 5672)
subscriber.start_subscriber()

@app.route('/main')
def stddev():
    stddev = subscriber.get_stddev()
    mean = subscriber.get_mean()
    if stddev is not None:
        return 'La desviación estándar es {:.2f}'.format(stddev, mean)
    else:
        return 'No hay suficientes datos para calcular la desviación estándar'

if __name__ == '__main__':
    app.run()
