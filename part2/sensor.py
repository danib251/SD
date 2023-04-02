import os
import sys
import time
import pika #pip install pika
import json

# Agregar el directorio utils al sys.path
utils_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils')
sys.path.append(utils_dir)

from meteo_utils import MeteoDataDetector


weather_data = MeteoDataDetector()

class Sensor:
    def __init__(self, sensor_id, server_address):
        self.sensor_id = sensor_id
        self.server_address = server_address
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_rmq = self.connection.channel()
        self.channel_rmq.queue_declare(queue='sensor_data')

    def send_data(self):
        
        meteo_data = weather_data.analyze_air()
        sensor_data1 = {
            'sensor_id': self.sensor_id,
            'time': int(time.time()),
            'weather_data': {
                'temperature': meteo_data['temperature'],
                'humidity': meteo_data['humidity']
            }
        }

        pollution_data = weather_data.analyze_pollution()
        sensor_data2 = {
            'sensor_id': self.sensor_id,
            'time': int(time.time()),
            'co2': pollution_data['co2']
        }

        print(f"Sending data from sensor {self.sensor_id}...")

        message = json.dumps(sensor_data1).encode('utf-8')
        message2 = json.dumps(sensor_data2).encode('utf-8')
        self.channel_rmq.basic_publish(exchange='', routing_key='sensor_data', body=message)
        #self.channel_rmq.basic_publish(exchange='', routing_key='sensor_data', body=message2)                                

        self.connection.close()


        
