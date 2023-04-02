import time
from sensor import Sensor

from meteo_utils import MeteoDataProcessor 
from meteo_utils import MeteoDataDetector 

if __name__ == '__main__':
    cont = 0
    while True:
        sensor = Sensor(sensor_id= cont, server_address= 'localhost:50051' )
        sensor.send_data() # Enviar datos al load balancer
        cont += 1
        time.sleep(1) # Esperar 10 segundos antes de enviar nuevos datos

    weather_data = MeteoDataDetector()
    processor = MeteoDataProcessor()

    # Generar 5 registros de datos de tiempo

    meteo_data = weather_data.analyze_air()
    pollution_data = weather_data.analyze_pollution()
    wellness_data = processor.process_meteo_data(meteo_data)
    
    pollution_data = processor.process_pollution_data(pollution_data)
    print(pollution_data)
