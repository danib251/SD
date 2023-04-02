import time

from sensor import Sensor


cont = 0
while True:
    sensor = Sensor(sensor_id= cont, server_address= 'localhost:50051' )
    sensor.send_data() # Enviar datos al load balancer
    cont += 1
    time.sleep(1) # Esperar 10 segundos antes de enviar nuevos datos