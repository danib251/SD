import redis
import pika
import json
import time

class IData:
    def process_data(self):
        pass

class RedisData(IData):
    def __init__(self, redis_host, redis_port):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    def process_data(self):
        if self.redis_client.llen('list') > 0:
            # Obtener el primer elemento de la lista
            first_element = self.redis_client.lpop('list')
            
            # Decodificar datos JSON
            air_data = json.loads(first_element)
            
            print("air_data:", air_data)
        
class RedisDataProxy(IData):
    def __init__(self, redis_data):
        self.redis_data = redis_data

    def process_data(self):
        print("\r%s" % "procesando datos", end="")
        self.redis_data.process_data()

class RabbitMQ:
    def __init__(self, rabbitmq_host, rabbitmq_port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='sensor_data')

    def publish_data(self, data):
        # Publicar datos en RabbitMQ
        self.channel.basic_publish(exchange='', routing_key='sensor_data', body=data)

class RedisDataProxyWithRabbitMQ(IData):
    def __init__(self, redis_data, rabbitmq):
        self.redis_data = redis_data
        self.rabbitmq = rabbitmq

    def process_data(self):
        self.redis_data.process_data()
        air_data = {"data": "air_processed", "id": "1", "time": time.time()}
        # Enviar resultados a RabbitMQ
        self.rabbitmq.publish_data(json.dumps(air_data))

def main():
    redis_data = RedisData('localhost', 6379)
    redis_data_proxy = RedisDataProxy(redis_data)
    rabbitmq = RabbitMQ('localhost', 5672)
    redis_data_proxy_with_rabbitmq = RedisDataProxyWithRabbitMQ(redis_data, rabbitmq)

    while True:
        redis_data_proxy.process_data()
        redis_data_proxy_with_rabbitmq.process_data()
        time.sleep(1)

if __name__ == '__main__':
    main()
