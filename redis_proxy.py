import json
import statistics

import redis
import grpc
import data_pb2
import data_pb2_grpc
import time


class DataServicer:
    def __init__(self, proxy_address):
        self.redis_client = redis.Redis()
        self.proxy_address = proxy_address
        self.channels = []  # lista de canales gRPC
        self.stubs = []  # lista de stubs gRPC
        self.sent_data = set()
        self.instance_id = None
        self.meteo_values = []
        self.pollution_values = []
        self.last_average_time = None

    def send_data(self):
        while True:
            pollution_data = self.redis_client.hgetall("pollution_data")
            meteo_data = self.redis_client.hgetall("meteo_data")

            pollution_data_dict = {k.decode(): v.decode() for k, v in pollution_data.items()}
            meteo_data_dict = {k.decode(): v.decode() for k, v in meteo_data.items()}

            for pollution_key, meteo_key in zip(pollution_data_dict.keys(), meteo_data_dict.keys()):
                if pollution_key not in self.sent_data and meteo_key not in self.sent_data:
                    meteo_value = json.loads(meteo_data_dict[meteo_key])["air_wellness"]
                    pollution_value = json.loads(pollution_data_dict[pollution_key])["pollution_coefficient"]
                    self.meteo_values.append(meteo_value)
                    self.pollution_values.append(pollution_value)
                    self.sent_data.add(pollution_key)
                    self.sent_data.add(meteo_key)

            # Calcular promedio cada 10 segundos
            if self.last_average_time is None or time.time() - self.last_average_time >= 10:
                if self.meteo_values and self.pollution_values:
                    meteo_average = statistics.mean(self.meteo_values)
                    pollution_average = statistics.mean(self.pollution_values)
                    print(f"Average meteo value: {meteo_average}")
                    print(f"Average pollution value: {pollution_average}")
                    data = data_pb2.Data(
                        pollution_data=json.dumps({"pollution_coefficient": pollution_average}),
                        meteo_data=json.dumps({"air_wellness": meteo_average})
                    )
                    # Enviar datos a todas las instancias de terminales
                    for stub in self.stubs:
                        stub.GetData(data)
                    self.meteo_values.clear()
                    self.pollution_values.clear()
                    self.last_average_time = time.time()

            time.sleep(1)

    def register_clients(self, num_clients):
        for i in range(num_clients):
            channel = grpc.insecure_channel(f"localhost:{50053 + i}")
            stub = data_pb2_grpc.DataRPCStub(channel)
            self.channels.append(channel)
            self.stubs.append(stub)


if __name__ == "__main__":
    data_servicer = DataServicer(proxy_address='localhost:50053')
    data_servicer.register_clients(num_clients=2)
    data_servicer.send_data()
