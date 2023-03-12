
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

class Sensor:
    def __init__(self, sensor_id, server_address):
        self.sensor_id = sensor_id
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = sensor_pb2_grpc.LoadBalancerStub(self.channel)

    def send_data(self):
        weather_data = MeteoDataDetector()
        meteo_data = weather_data.analyze_air()
        
        info = sensor_pb2.MeteoData(
            sensor_id=self.sensor_id,
            temperature = meteo_data['temperature'],
            humidity = meteo_data['humidity'],
            timestamp = timestamp_pb2.Timestamp()
        )
        pollution_data = weather_data.analyze_pollution()
        info2 = sensor_pb2.PollutionData(
            sensor_id=self.sensor_id,
            co2=pollution_data['co2'],
            timestamp = timestamp_pb2.Timestamp()
        )

        print(f"Sending data from sensor {self.sensor_id}...")
        self.stub.ProcessMeteoData(info)
        self.stub.ProcessPollutionData(info2)


        

"""
class Sensor:
    def __init__(self, sensor_id, sensor_type, lb_host, lb_port, sleep_time=10):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.lb_host = lb_host
        self.lb_port = lb_port
        self.sleep_time = sleep_time

    def start(self):
        while True:
            # Get raw data from the sensor
            if self.sensor_type == 'meteo':
                raw_data = meteo_utils.MeteoDataDetector().get_raw_meteo_data()
            elif self.sensor_type == 'pollution':
                raw_data = meteo_utils.PollutionDataDetector().get_raw_pollution_data()
                
            # Send the data to the load balancer
            lb_client = LBClient(self.lb_host, self.lb_port)
            lb_client.send_data(self.sensor_id, self.sensor_type, raw_data)

            # Wait for some time before sending the next record
            time.sleep(self.sleep_time)
    

    
    En este código, la clase Sensor recibe los siguientes argumentos:

sensor_id: ID único del sensor.
sensor_type: Tipo de sensor ('meteo' o 'pollution').
lb_host: Dirección IP o hostname del servidor del Load Balancer.
lb_port: Puerto del servidor del Load Balancer.
sleep_time: Tiempo de espera en segundos entre cada envío de datos.
La clase tiene un método start que se ejecuta en un bucle infinito. En cada iteración, 
se obtiene el raw data del sensor correspondiente usando la clase MeteoDataDetector o PollutionDataDetector de meteo_utils.
A continuación, se envía el raw data al Load Balancer usando la clase LBClient, que aún no hemos definido. Por último, 
se espera el tiempo definido en sleep_time antes de la siguiente iteración.

    """