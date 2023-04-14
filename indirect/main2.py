import time
from sensor2 import Sensor
import os
import webbrowser

# Solicitar la cantidad de sensores que el usuario desea ejecutar
num_sensores = int(input("Ingrese la cantidad de sensores que desea ejecutar: ")) #un 2 per exemple
# Solicitar la cantidad de servidores que el usuario desea ejecutar
num_servers = int(input("Ingrese la cantidad de servidores que desea ejecutar: ")) # un 3 per exemple necesites tot lo del redis

# Solicitar la cantidad de terminales que el usuario desea ejecutar
num_terminales = int(input("Ingrese la cantidad de terminales que desea ejecutar: ")) # un 3 per exemple necesites tot lo del redis

# Ejecutar los archivos "sensor.py" y "rabbitserver.py"
port = '500'
url = 'http://localhost:'
if os.name == 'nt':  # Windows
    os.system(f'start cmd.exe /c "python RedisDataProxy.py"')
    for i in range(num_servers):
        os.system(f'start cmd.exe /c "python rabbitserver.py {"sensor_data"}"')
    for i in range(num_terminales):
        id = port + str(i+1)
        os.system(f'start cmd.exe /c "python terminal.py {id}"')
        webbrowser.open(url + id)
    
        
elif os.name == 'posix':  # Linux o macOS
    current_dir = os.getcwd()

    #os.system(f'gnome-terminal -- python rabbitserver.py {"sensor_data"}')
    #os.system(f'gnome-terminal -- python RedisDataProxy.py {num_terminales}')
    os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python RedisDataProxy.py {num_terminales}"\'')
    for i in range(num_servers):
        os.system(
            f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python rabbitserver.py {"sensor_data"}"\'')
    for i in range(num_terminales):
        id = port + str(i+1) 
        os.system(f'osascript -e \'tell app "Terminal" to do script "cd {current_dir} && python terminal.py {id}"\'')
        webbrowser.open(url + id)
else:
    print("Sistema operativo no compatible")


sensors = [Sensor(i) for i in range(num_sensores)]
while True:

    for sensor in sensors:
        sensor.send_data() 
        time.sleep(0.5)    

    