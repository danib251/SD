import redis
import json
from datetime import datetime

class StorageServer:
    def __init__(self, host='localhost', port=6379):
        self.db = redis.Redis(host=host, port=port)

    def save_meteo_data(self, data, timestamp):
        # Guarda los datos procesados en Redis
        key = f"processed_meteo_data_{timestamp}"
        self.db.set(key, json.dumps(data))

    def save_pollution_data(self, data, timestamp):
        # Guarda los datos procesados en Redis
        key = f"processed_pollution_data_{timestamp}"
        self.db.set(key, json.dumps(data))

    def get_mean_meteo_data(self, start_time, end_time):
        # Calcula el promedio de los datos procesados en el intervalo de tiempo especificado
        keys = self.db.keys("processed_meteo_data_*")
        values = []
        for key in keys:
            timestamp_str = key.decode('utf-8').split('_')[-1]
            timestamp = datetime.fromisoformat(timestamp_str)
            if start_time <= timestamp <= end_time:
                data = json.loads(self.db.get(key).decode('utf-8'))
                values.append(data)
        if values:
            return {
                'temperature_mean': sum([d['temperature'] for d in values])/len(values),
                'humidity_mean': sum([d['humidity'] for d in values])/len(values)
            }
        else:
            return None

    def get_mean_pollution_data(self, start_time, end_time):
        # Calcula el promedio de los datos procesados en el intervalo de tiempo especificado
        keys = self.db.keys("processed_pollution_data_*")
        values = []
        for key in keys:
            timestamp_str = key.decode('utf-8').split('_')[-1]
            timestamp = datetime.fromisoformat(timestamp_str)
            if start_time <= timestamp <= end_time:
                data = json.loads(self.db.get(key).decode('utf-8'))
                values.append(data)
        if values:
            return {'co2_mean': sum([d['co2'] for d in values])/len(values)}
        else:
            return None
