import argparse
import json
from concurrent import futures
import google.protobuf
import grpc
from matplotlib import pyplot as plt

import data_pb2_grpc
from rich.console import Console

console = Console()


class Terminal(data_pb2_grpc.DataRPCServicer):
    def __init__(self):
        self.meteo_data = []
        self.pollution_data = []

    def GetData(self, request, context):
        console.print(
            f"Received data: [bold]Pollution[/bold] - {request.pollution_data}, [bold]Meteo[/bold] - {request.meteo_data}, [bold]Timestamp[/bold] - {request.timestamp}")
        self.meteo_data.append((json.loads(request.meteo_data))['air_wellness'])
        self.pollution_data.append((json.loads(request.pollution_data))['pollution_coefficient'])
        plt.ion()
        fig, axs = plt.subplots(2)

        axs[0].clear()
        axs[0].plot(self.meteo_data, label='Meteo data')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Air Wellness')
        axs[0].legend()

        axs[1].clear()
        axs[1].plot(self.pollution_data, label='Pollution data')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Pollution')
        axs[1].legend()

        plt.draw()
        plt.pause(0.001)

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
