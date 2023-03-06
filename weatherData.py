from meteo_utils import MeteoDataDetector
from datetime import datetime
class WeatherData:
    def __init__(self):
        self.detector = MeteoDataDetector()

    def generate_data(self):
        temperature = self.detector.gen_temperature()
        humidity = self.detector.gen_humidity()
        timestamp = datetime.now()
        meteodata = MeteoDataDetector(temperature=temperature, humidity=humidity, timestamp=timestamp)
        return meteodata