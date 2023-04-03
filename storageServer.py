import grpc
import redis
import json
from datetime import datetime
from concurrent import futures

import server_pb2_grpc
import google.protobuf


class StorageServer(server_pb2_grpc.ServerServicer):
    def __init__(self, servers):
        self.servers = servers
        self.server_index = 0
        self.sensor_id = 0
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def ReceivedMeteoData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)
        print("Got request " + str(request))
        data = {"lb_id": request.lb_id, "air_wellness": request.air_wellness}
        self.redis_client.hmset("meteo_data", {str(datetime.now()): json.dumps(data)})
        return google.protobuf.empty_pb2.Empty()


    def ReceivedPollutionData(self, request, context):
        # Choose a server in round-robin fashion
        server = self.servers[self.server_index]
        self.server_index = (self.server_index + 1) % len(self.servers)
        print("Got request " + str(request))
        data = {"lb_id": request.lb_id, "pollution_coefficient": request.pollution_coefficient}
        self.redis_client.hmset("pollution_data", {str(datetime.now()): json.dumps(data)})
        return google.protobuf.empty_pb2.Empty()



def server():
    # Create a gRPC server and add the LoadBalancerServicer
    cont = 0
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    server_pb2_grpc.add_ServerServicer_to_server(StorageServer(["Server1", "Server2"]), server)

    # Bind the server to a port and start it
    server.add_insecure_port('[::]:50052')
    print("gRPC server starting...")
    server.start()

    # Wait for the server to terminate
    server.wait_for_termination()


if __name__ == '__main__':
    server()
