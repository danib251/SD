import pika
import json
import meteo_utils

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sensor_data')


def callback(ch, method, properties, body):
    data = json.loads(body)
    if 'weather_data' in data:
        # Procesar datos del tipo 1
        weather_data = data['weather_data']
        # Calculates the air_wellness
        processor = meteo_utils.MeteoDataProcessor()
        w = {
                'temperature': 1,
                'humidity': 2
            }
      
        
        air_processed = processor.process_meteo_data(w)
        print("Datos del tipo 1 - Weather data:", air_processed)
    elif 'co2' in data:
        # Procesar datos del tipo 2
        co2 = data['co2']
        # Calculates the air_wellness
        processor = meteo_utils.MeteoDataProcessor()
        air_processed = processor.process_pollution_data(co2)
        print("Datos del tipo 2 - Pollution data:", air_processed)
    else:
        print("Mensaje no identificado:", data)

channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)

print("Starting Consuming")
channel.start_consuming()