from concurrent import futures

import google.protobuf
import grpc
import data_pb2
import data_pb2_grpc


class Terminal(data_pb2_grpc.DataRPCServicer):
    def GetData(self, request, context):
        print(request)
        return google.protobuf.empty_pb2.Empty()

def server():
    # Create a gRPC server and add the LoadBalancerServicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    data_pb2_grpc.add_DataRPCServicer_to_server(Terminal(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    print("gRPC server starting...")
    server.wait_for_termination()


if __name__ == "__main__":
    server()
