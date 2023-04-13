import pika
import json
import redis
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("queue", help="Nombre de la cola a la que se suscribirá el consumidor")
args = parser.parse_args()
print("Suscribiendo consumidor a la cola:", args.queue)

utils_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils')
sys.path.append(utils_dir)
import meteo_utils

# Conexión a Redis
redis_client = redis.Redis()
# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=args.queue)


def callback(ch, method, properties, body):
    data = json.loads(body)
    id = data['sensor_id']
    time = data['time']
    processor = meteo_utils.MeteoDataProcessor()
    if 'weather_data' in data:
        # Procesar datos del tipo 1
        weather_data = data['weather_data']
        # Calculates the air_wellness
        air_processed = processor.process_meteo_data(weather_data)
        #print("Datos del tipo 1 - Weather data:", air_processed)
        print(" [x] Received %r" % body)
        redis_client.rpush('list', json.dumps({"air_wellness": air_processed, "id": id, "time": time}))

    elif 'co2' in data:
        # Procesar datos del tipo 2
        co2 = data['co2']
        # Calculates the air_wellness
        pollution_processed = processor.process_pollution_data(co2)
        print(" [x] Received %r" % body)
        redis_client.rpush('list', json.dumps({"co2_wellness": pollution_processed, "id": id, "time": time}))

    else:
        print("Mensaje no identificado:", data)

channel.basic_consume(queue=args.queue, on_message_callback=callback, auto_ack=True)

print("Starting Consuming")
channel.start_consuming()