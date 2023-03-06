from meteo_utils import MeteoDataDetector

class WeatherData:
    def __init__(self):
        self.detector = MeteoDataDetector()

    def generate_data(self):
        return self.detector.gen_temperature()