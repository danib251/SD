# %%
import os
import time
from sensor import Sensor

from meteo_utils import MeteoDataProcessor
from meteo_utils import MeteoDataDetector

if __name__ == '__main__':
    cont = 0
    num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: "))
    num_servers = int(input("Ingrese la cantidad de storage servers que desea ejecutar: "))
    num_terminales = int(
        input("Ingrese la cantidad de terminales que desea ejecutar: "))

    if os.name == 'nt':  # Windows
        os.system(f'start cmd.exe /c "python load_balancer.py {num_servers}"')
        for i in range(num_servers):
            os.system(f'start cmd.exe /c "python storageServer.py {i}"')
        for i in range(num_terminales):
            os.system(f'start cmd.exe /c "python terminal.py {i}"')
        os.system(f'start cmd.exe /c "python redis_proxy.py {num_terminales}"')
    elif os.name == 'posix':  # Linux o macOS
        current_dir = os.getcwd()

        # os.system(f'gnome-terminal -- python rabbitserver.py {"sensor_data"}')
        # os.system(f'gnome-terminal -- python RedisDataProxy.py {num_terminales}')
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python load_balancer.py {num_servers}"\'')
        for i in range(num_servers):
            os.system(
                f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python storageServer.py {i}"\'')
        time.sleep(2)
        for i in range(num_terminales):
            os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python terminal.py {i}"\'')
        time.sleep(2)
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python redis_proxy.py {num_terminales}"\'')

    else:
        print("Sistema operativo no compatible")
    
    sensores = []
    for i in range(num_sensores):
        sensor = Sensor(sensor_id=i, data_id=cont, server_address='localhost:50051')
        sensores.append(sensor)
        cont += 1

    while True:
        for sensor in sensores:
            sensor.send_data()  # Enviar datos al load balancer
        time.sleep(1)
