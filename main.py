
from meteo_utils import MeteoDataProcessor 
from meteo_utils import MeteoDataDetector 

if __name__ == '__main__':
    weather_data = MeteoDataDetector()
    processor = MeteoDataProcessor()

    # Generar 5 registros de datos de tiempo

    meteo_data = weather_data.analyze_air()
    pollution_data = weather_data.analyze_pollution()
    wellness_data = processor.process_meteo_data(meteo_data)
    
    pollution_data = processor.process_pollution_data(pollution_data)
    print(pollution_data)
        

    
    
    