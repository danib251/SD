
import time
import grpc
from meteo_utils import MeteoDataDetector

# pip install grpcio-tools
import time
import grpc
from meteo_utils import MeteoDataDetector
import sensor_pb2 as sensor_pb2
import sensor_pb2_grpc as sensor_pb2_grpc
from datetime import datetime
import google.protobuf.timestamp_pb2 as timestamp_pb2
import pika #pip install pika
import json


class Sensor:
    def __init__(self, sensor_id, server_address):
        self.sensor_id = sensor_id
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = sensor_pb2_grpc.LoadBalancerStub(self.channel)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel_rmq = self.connection.channel()
        self.channel_rmq.queue_declare(queue='sensor_data')

    def send_data(self):
        weather_data = MeteoDataDetector()
        meteo_data = weather_data.analyze_air()

        info = sensor_pb2.MeteoData(
            sensor_id=self.sensor_id,
            meteo_data=sensor_pb2.TempHumidity(
                temperature=meteo_data['temperature'],
                humidity=meteo_data['humidity']
            ),
            timestamp=timestamp_pb2.Timestamp()
        )

        sensor_data1 = {
            'sensor_id': self.sensor_id,
            'time': int(time.time()),
            'weather_data': {
                'temperature': meteo_data['temperature'],
                'humidity': meteo_data['humidity']
            }
        }

        pollution_data = weather_data.analyze_pollution()
        info2 = sensor_pb2.PollutionData(
            sensor_id=self.sensor_id,
            co2=pollution_data['co2'],
            timestamp=timestamp_pb2.Timestamp()
        )

        sensor_data2 = {
            'sensor_id': self.sensor_id,
            'time': int(time.time()),
            'co2': pollution_data['co2']
        }
        
        
        

        print(f"Sending data from sensor {self.sensor_id}...")
        #self.stub.ProcessMeteoData(info)
        #self.stub.ProcessPollutionData(info2)
        message = json.dumps(sensor_data1).encode('utf-8')
        message2 = json.dumps(sensor_data2).encode('utf-8')
        self.channel_rmq.basic_publish(exchange='', routing_key='sensor_data', body=message)
        #self.channel_rmq.basic_publish(exchange='', routing_key='sensor_data', body=message2)                                
        ##self.channel_rmq.basic_publish(exchange='', routing_key='sensor_data', body=info2.SerializeToString())

        self.connection.close()


        
