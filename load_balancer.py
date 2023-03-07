import xmlrpc.server
import xmlrpc.client
import meteo_utils  # importe las funciones necesarias de util.py

class LoadBalancer:
    def __init__(self, server_list):
        # inicializar las variables necesarias, como los puertos de escucha y la lista de servidores
        self.server_list = server_list

    def register_server(self, server_info):
        # agregar el servidor a la lista de servidores conocidos
        self.server_list.append(server_info)

    def process_data(self, sensor_id, data):
    # seleccionar el servidor adecuado para procesar los datos en un patrón round-robin
        server_info = self.server_list.pop(0)
        self.server_list.append(server_info)

        # enviar la solicitud al servidor seleccionado y devolver la respuesta
        with xmlrpc.client.ServerProxy(server_info['url']) as server:
            if sensor_id.startswith('M'):
                result = server.process_meteo_data(data)
            elif sensor_id.startswith('P'):
                result = server.process_pollution_data(data)
            else:
                raise ValueError("Invalid sensor ID")

        return result


if __name__ == '__main__':
    # establecer los detalles de conexión y configuración del servidor RPC
    server_list = []  # lista de servidores conocidos
    lb = LoadBalancer(server_list)
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000))
    server.register_instance(lb)

    # iniciar el servidor RPC y escuchar las solicitudes entrantes
    print("Load balancer listening on port 8000...")
    server.serve_forever()
