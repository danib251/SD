import random
import grpc
import time

import meteo_utils
import sensor_pb2
import sensor_pb2_grpc
import google.protobuf.empty_pb2
from concurrent import futures


class LoadBalancer(sensor_pb2_grpc.LoadBalancerServicer):
    def __init__(self, servers):
        self.servers = servers
        self.server_index = 0

    def ProcessMeteoData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)

        # Content of the request
        print("Got request " + str(request))

        # Calculates the air_wellness
        processor = meteo_utils.MeteoDataProcessor()
        air_wellness = processor.process_meteo_data(request.meteo_data)

        # Connect to server and sends data
        print(f"Processing meteo data on server {server}")

        # TODO Connect to server and send the processed data

        return google.protobuf.empty_pb2.Empty()

    def ProcessPollutionData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)

        # Content of the request
        print("Got request " + str(request))

        # Calculates the pollution coefficient
        processor = meteo_utils.MeteoDataProcessor()
        pollution_coefficient = processor.process_pollution_data(request.co2)
        print(pollution_coefficient)

        # TODO Connect to server and send the processed data

        # Connect to server and process data
        print(f"Processing pollution data on server {server}")
        return google.protobuf.empty_pb2.Empty()


def server():
    # Create a gRPC server and add the LoadBalancerServicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    sensor_pb2_grpc.add_LoadBalancerServicer_to_server(LoadBalancer(["Server1", "Server2"]), server)

    # Bind the server to a port and start it
    server.add_insecure_port('[::]:50051')
    print("gRPC server starting...")
    server.start()

    # Wait for the server to terminate
    server.wait_for_termination()


if __name__ == '__main__':
    server()
