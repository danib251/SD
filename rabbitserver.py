import pika
import json
import meteo_utils
import redis

# Conexión a Redis
redis_client = redis.Redis()
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')


def callback(ch, method, properties, body):
    data = json.loads(body)
    processor = meteo_utils.MeteoDataProcessor()
    if 'weather_data' in data:
        # Procesar datos del tipo 1
        weather_data = data['weather_data']
        id = data['sensor_id']
        time = data['time']
        # Calculates the air_wellness
        air_processed = processor.process_meteo_data(weather_data)
        #print("Datos del tipo 1 - Weather data:", air_processed)
        print(" [x] Received %r" % body)
        redis_client.rpush('list', json.dumps({"data": air_processed, "id": id, "time": time}))

    elif 'co2' in data:
        # Procesar datos del tipo 2
        co2 = data['co2']
        # Calculates the air_wellness
        pollution_processed = processor.process_pollution_data(co2)
        print("Datos del tipo 2 - Pollution data:", pollution_processed)
        #print(" [x] Received %r" % body)
        redis_client.set("pollution_processed", json.dumps(pollution_processed))

    else:
        print("Mensaje no identificado:", data)

channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

print("Starting Consuming")
channel.start_consuming()