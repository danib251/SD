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

    def send_data(self):
        while True:
            pollution_data = self.redis_client.hgetall("pollution_data")
            meteo_data = self.redis_client.hgetall("meteo_data")

            pollution_data_dict = {k.decode(): v.decode() for k, v in pollution_data.items()}
            meteo_data_dict = {k.decode(): v.decode() for k, v in meteo_data.items()}

            for pollution_key, meteo_key in zip(pollution_data_dict.keys(), meteo_data_dict.keys()):
                if pollution_key not in self.sent_data and meteo_key not in self.sent_data:
                    print(pollution_key, ":", pollution_data_dict[pollution_key])
                    print(meteo_key, ":", meteo_data_dict[meteo_key])
                    data = data_pb2.Data(
                        pollution_data=pollution_data_dict[pollution_key],
                        meteo_data=meteo_data_dict[meteo_key]
                    )
                    # Enviar datos a todas las instancias de terminales
                    print(self.stubs)
                    for stub in self.stubs:
                        stub.GetData(data)
                    self.sent_data.add(pollution_key)
                    self.sent_data.add(meteo_key)
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
