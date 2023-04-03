import time

from sensor import Sensor

import os

# Solicitar la cantidad de sensores que el usuario desea ejecutar
num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: "))

# Solicitar la cantidad de terminales que el usuario desea ejecutar
num_terminales = int(input("Ingrese la cantidad de terminales que desea ejecutar: "))

# Ejecutar los archivos "sensor.py" y "rabbitserver.py"

queue_name = "sensor_data"
os.system(f'start cmd.exe /c "python rabbitserver.py {queue_name}"')

os.system(f'start cmd.exe /c "python RedisDataProxy.py {num_terminales}"')

cont = 0
while True:
    print(num_sensores)
    sensor = Sensor(sensor_id= cont, server_address= 'localhost:50051' )

    sensor.send_data() # Enviar datos al load balancer
    cont += 1
    time.sleep(1) # Esperar 10 segundos antes de enviar nuevos datos