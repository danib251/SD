import time
from sensor import Sensor
import os

# Solicitar la cantidad de sensores que el usuario desea ejecutar
num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: ")) #un 2 per exemple
# Solicitar la cantidad de terminales que el usuario desea ejecutar
num_terminales = int(input("Ingrese la cantidad de terminales que desea ejecutar: ")) # un 3 per exemple necesites tot lo del redis


data_sensor = 'sensor_data_'
queue_name = data_sensor + str(num_terminales)

# Ejecutar los archivos "sensor.py" y "rabbitserver.py"

if os.name == 'nt':  # Windows
    os.system(f'start cmd.exe /c "python rabbitserver.py {"sensor_data"}"')
    os.system(f'start cmd.exe /c "python RedisDataProxy.py"')
    for i in range(num_terminales):
        queue_name = data_sensor + str(i+1)
        #os.system(f'start cmd.exe /c "python terminal.py"')
elif os.name == 'posix':  # Linux o macOS
    current_dir = os.getcwd()

    #os.system(f'gnome-terminal -- python rabbitserver.py {"sensor_data"}')
    #os.system(f'gnome-terminal -- python RedisDataProxy.py {num_terminales}')
    os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python rabbitserver.py sensor_data"\'')
    os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python RedisDataProxy.py {num_terminales}"\'')
    for i in range(num_terminales):
        queue_name = data_sensor + str(i+1)
        os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python terminal.py"\'')
else:
    print("Sistema operativo no compatible")


sensors = [Sensor(i, server_address='localhost:50051') for i in range(num_sensores)]
while True:

    for sensor in sensors:
        sensor.send_data() 
        time.sleep(1)    

    