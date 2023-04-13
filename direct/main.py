import os
import time
from sensor import Sensor

from meteo_utils import MeteoDataProcessor
from meteo_utils import MeteoDataDetector

if __name__ == '__main__':
    cont = 0
    num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: "))
    num_terminales = int(
        input("Ingrese la cantidad de terminales que desea ejecutar: "))

    data_sensor = 'sensor_data_'
    queue_name = data_sensor + str(num_terminales)

    if os.name == 'nt':  # Windows
        os.system(f'start cmd.exe /c "python load_balancer.py"')
        os.system(f'start cmd.exe /c "python storageServer.py"')
        os.system(f'start cmd.exe /c "python redis_proxy.py"')
        for i in range(num_terminales):
            queue_name = data_sensor + str(i + 1)
            os.system(f'start cmd.exe /c "python terminal.py"')
    elif os.name == 'posix':  # Linux o macOS
        current_dir = os.getcwd()

        # os.system(f'gnome-terminal -- python rabbitserver.py {"sensor_data"}')
        # os.system(f'gnome-terminal -- python RedisDataProxy.py {num_terminales}')
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir}/direct && python load_balancer.py"\'')
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir}/direct && python storageServer.py"\'')
        time.sleep(2)
        for i in range(num_terminales):
            queue_name = data_sensor + str(i + 1)
            os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir}/direct && python terminal.py {i}"\'')
        time.sleep(2)
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir}/direct && python redis_proxy.py {num_terminales}"\'')

    else:
        print("Sistema operativo no compatible")

    while True:
        sensor = Sensor(sensor_id= cont, server_address= 'localhost:50051' )
        sensor.send_data() # Enviar datos al load balancer
        cont += 1
        time.sleep(1) # Esperar 10 segundos antes de enviar nuevos datos
