import redis
import pika
import json

import time

class RedisDataProxy:
    def __init__(self, redis_host, redis_port, rabbitmq_host, rabbitmq_port):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='sensor_data')

    def process_data(self):
        # Obtener datos de Redis y procesarlos
        #air_data = self.redis_client.get('air_processed')
        #pollution_data = self.redis_client.get('pollution_processed')


        if self.redis_client.llen('list') > 0:
            # Obtener el primer elemento de la lista
            first_element = self.redis_client.lpop('list')
            
            # Decodificar datos JSON
            air_data = json.loads(first_element)
            
            print("air_data:", air_data)
        
        #pollution_data = json.loads(pollution_data)
        #print("pollution_data:", pollution_data)
        # ...
        # Enviar resultados a RabbitMQ
        # ...
        print("\r%s" % "procesando datos", end="")
        
    def run(self, interval=1):
        # Ejecutar continuamente la función de procesamiento de datos
        while True:
            self.process_data()
            time.sleep(interval)
if __name__ == '__main__':
    proxy = RedisDataProxy('localhost', 6379, 'localhost', 5672)
    proxy.run()
