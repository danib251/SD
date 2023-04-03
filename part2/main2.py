import time
from sensor import Sensor
import os

# Solicitar la cantidad de sensores que el usuario desea ejecutar
num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: "))
# Solicitar la cantidad de terminales que el usuario desea ejecutar
num_terminales = int(input("Ingrese la cantidad de terminales que desea ejecutar: "))

# Ejecutar los archivos "sensor.py" y "rabbitserver.py"

if os.name == 'nt':  # Windows
    os.system(f'start cmd.exe /c "python rabbitserver.py {"sensor_data"}"')
    os.system(f'start cmd.exe /c "python RedisDataProxy.py {num_terminales}"')
elif os.name == 'posix':  # Linux o macOS
    os.system(f'gnome-terminal -- python rabbitserver.py {"sensor_data"}')
    os.system(f'gnome-terminal -- python RedisDataProxy.py {num_terminales}')
else:
    print("Sistema operativo no compatible")


sensors = [Sensor(i, server_address='localhost:50051') for i in range(num_sensores)]
while True:

    for sensor in sensors:
        sensor.send_data() 
    time.sleep(1)

    