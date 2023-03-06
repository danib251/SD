from weatherData import WeatherData
from meteo_utils import MeteoDataProcessor

if __name__ == '__main__':
    weather_data = WeatherData()
    processor = MeteoDataProcessor()

    # Generar 5 registros de datos de tiempo

    for i in range(5):
        data = weather_data.generate_data()
        print(f"Registro {i+1}: Temperatura {data.temperature}")
        wellness_data = processor.process_meteo_data(data)
        

    
    
    