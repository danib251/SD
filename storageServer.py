import grpc
import redis
import json
from datetime import datetime
from concurrent import futures

import server_pb2_grpc


class StorageServer(server_pb2_grpc.ServerServicer):
    def __init__(self, servers):
        self.servers = servers
        self.server_index = 0
        self.sensor_id = 0

    def ReceivedMeteoData(self, request, context):
        # Choose a server in round-robin fashion
        print("HEY")

    def ReceivedPollutionData(self, request, context):
        print("HEY")

def server():
    # Create a gRPC server and add the LoadBalancerServicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    server_pb2_grpc.add_ServerServicer_to_server(StorageServer(["Server1", "Server2"]), server)

    # Bind the server to a port and start it
    server.add_insecure_port('[::]:50051')
    print("gRPC server starting...")
    server.start()

    # Wait for the server to terminate
    server.wait_for_termination()


if __name__ == '__main__':
    server()