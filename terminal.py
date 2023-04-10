import argparse
from concurrent import futures

import google.protobuf
import grpc
import data_pb2
import data_pb2_grpc
from rich.console import Console

console = Console()


class Terminal(data_pb2_grpc.DataRPCServicer):
    def GetData(self, request, context):
        console.print(f"Received data: [bold]Pollution[/bold] - {request.pollution_data}, [bold]Meteo[/bold] - {request.meteo_data}, [bold]Timestamp[/bold] - {request.timestamp}")
        return google.protobuf.empty_pb2.Empty()


def server(instance_id):
    port = 50053 + instance_id
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    data_pb2_grpc.add_DataRPCServicer_to_server(Terminal(), server)
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    console.print(f"gRPC server starting on port {port}...")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Terminal instance')
    parser.add_argument('id', type=int, help='an integer ID for the terminal instance')
    args = parser.parse_args()
    server(args.id)
