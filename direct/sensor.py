# pip install grpcio-tools
import sys
import time
import grpc
from meteo_utils import MeteoDataDetector
import sensor_pb2 as sensor_pb2
import sensor_pb2_grpc as sensor_pb2_grpc


class Sensor:
    def __init__(self, sensor_id, data_id, server_address):
        self.sensor_id = sensor_id
        self.data_id = data_id
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = sensor_pb2_grpc.LoadBalancerStub(self.channel)

    def send_data(self):
        weather_data = MeteoDataDetector()
        meteo_data = weather_data.analyze_air()
        if self.data_id % 2 == 0:
            info = sensor_pb2.MeteoData(
                sensor_id=self.data_id,
                meteo_data=sensor_pb2.TempHumidity(
                    temperature=meteo_data['temperature'],
                    humidity=meteo_data['humidity']
                ),
                timestamp=int(time.time())
            )
            print(f"Sending meteo data from sensor {self.sensor_id}...")
            self.stub.ProcessMeteoData(info)

        else:
            pollution_data = weather_data.analyze_pollution()
            info = sensor_pb2.PollutionData(
                sensor_id=self.data_id,
                co2=pollution_data['co2'],
                timestamp=int(time.time())
            )
            print(f"Sending pollution data from sensor {self.sensor_id}...")
            self.stub.ProcessPollutionData(info)

