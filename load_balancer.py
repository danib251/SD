import random
import grpc
import time

from google.protobuf import timestamp_pb2

import meteo_utils
import sensor_pb2
import sensor_pb2_grpc
import google.protobuf.timestamp_pb2 as timestamp_pb2
from concurrent import futures
import google.protobuf

import server_pb2
import server_pb2_grpc


class LoadBalancer(sensor_pb2_grpc.LoadBalancerServicer):
    lb_id = 0

    def __init__(self, servers, server_address):
        self.servers = servers
        self.server_address = server_address
        self.server_index = 0
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = server_pb2_grpc.ServerStub(self.channel)

    def ProcessMeteoData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)

        LoadBalancer.lb_id += 1

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
            timestamp=timestamp_pb2.Timestamp()
        )
        print(f"Sending data from LB {self.lb_id}...")
        self.stub.ReceivedMeteoData(info)

        return google.protobuf.empty_pb2.Empty()

    def ProcessPollutionData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)

        LoadBalancer.lb_id += 1

        # Content of the request
        print("Got request " + str(request))

        # Calculates the pollution coefficient
        processor = meteo_utils.MeteoDataProcessor()
        pollution_processed = processor.process_pollution_data(request.co2)

        info = server_pb2.ProcessedPollutionData(
            lb_id=self.lb_id,
            pollution_coefficient=pollution_processed,
            timestamp=timestamp_pb2.Timestamp()
        )
        print(f"Sending data from LB {self.lb_id}...")
        self.stub.ReceivedPollutionData(info)

        # Connect to server and process data
        print(f"Processing pollution data on server {server}")
        return google.protobuf.empty_pb2.Empty()


def server():
    cont = 0
    # Create a gRPC server and add the LoadBalancerServicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    sensor_pb2_grpc.add_LoadBalancerServicer_to_server(LoadBalancer(["Server1", "Server2"], 'localhost:50052'), server)
    cont += 1

    # Bind the server to a port and start it
    server.add_insecure_port('[::]:50052')
    print("gRPC server starting...")
    server.start()

    # Wait for the server to terminate
    server.wait_for_termination()


if __name__ == '__main__':
    server()
