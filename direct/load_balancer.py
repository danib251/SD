import sys

import grpc
import time

from google.protobuf import timestamp_pb2

import meteo_utils
import sensor_pb2_grpc
from concurrent import futures
import google.protobuf

import server_pb2
import server_pb2_grpc


class LoadBalancer(sensor_pb2_grpc.LoadBalancerServicer):
    lb_id = 0

    def __init__(self, server_address):
        self.server_address = server_address
        self.server_index = 0
        self.channels = []
        self.stubs = []
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = server_pb2_grpc.ServerStub(self.channel)
        self.num_stubs = int(sys.argv[1])
        self.queue_stubs = 0

    def ProcessMeteoData(self, request, context):
        LoadBalancer.lb_id += 1

        if len(self.stubs) != self.num_stubs:
            LoadBalancer.register_clients(self, num_clients=self.num_stubs)

        print(len(self.stubs))

        # Content of the request
        print("Got request " + str(request))

        # Calculates the air_wellness
        processor = meteo_utils.MeteoDataProcessor()
        air_processed = processor.process_meteo_data(request.meteo_data)

        # Connect to server and sends data
        print(f"Processing meteo data on server {server}")

        info = server_pb2.ProcessedMeteoData(
            lb_id=self.lb_id,
            air_wellness=air_processed,
            timestamp=int(time.time())
        )
        print(f"Sending data from LB {self.lb_id}...")
        self.stubs[self.queue_stubs % self.num_stubs].ReceivedMeteoData(info)
        self.queue_stubs += 1

        return google.protobuf.empty_pb2.Empty()

    def ProcessPollutionData(self, request, context):
        LoadBalancer.lb_id += 1

        if len(self.stubs) != self.num_stubs:
            LoadBalancer.register_clients(self, num_clients=self.num_stubs)

        print(len(self.stubs))

        # Content of the request
        print("Got request " + str(request))

        # Calculates the pollution coefficient
        processor = meteo_utils.MeteoDataProcessor()
        pollution_processed = processor.process_pollution_data(request.co2)

        info = server_pb2.ProcessedPollutionData(
            lb_id=self.lb_id,
            pollution_coefficient=pollution_processed,
            timestamp=int(time.time())
        )
        print(f"Sending data from LB {self.lb_id}...")
        self.stubs[self.queue_stubs % self.num_stubs].ReceivedPollutionData(info)
        self.queue_stubs += 1

        # Connect to server and process data
        print(f"Processing pollution data on server {server}")
        return google.protobuf.empty_pb2.Empty()

    def register_clients(self, num_clients):
        for i in range(num_clients):
            channel = grpc.insecure_channel(f"localhost:{50056 + i}")
            stub = server_pb2_grpc.ServerStub(channel)
            self.channels.append(channel)
            self.stubs.append(stub)
            print(f'Numero de stubs: {len(self.stubs)}')


def server():
    cont = 0
    # Create a gRPC server and add the LoadBalancerServicer
    load_balancer = LoadBalancer(server_address='localhost:50056')
    load_balancer.register_clients(num_clients=int(sys.argv[1]))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    sensor_pb2_grpc.add_LoadBalancerServicer_to_server(LoadBalancer('localhost:50056'), server)

    # cont += 1

    # Bind the server to a port and start it
    server.add_insecure_port('[::]:50051')
    print("gRPC server starting...")
    server.start()

    # Wait for the server to terminate
    server.wait_for_termination()


if __name__ == '__main__':
    server()
