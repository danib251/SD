import redis
import pika
import json
import time
import sys
import statistics

class IData:
    def process_data(self):
        pass

class RedisData(IData):
    def __init__(self, redis_host, redis_port, window_size):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.window_size = window_size
    def process_data(self):
        air_data_list = []
        co2_data_list = []
        air_data_mean = -1
        co2_data_mean = -1
        list_elements = self.redis_client.lrange('list', 0, self.window_size - 1)
        if len(list_elements) > 0:
            # Decodificar datos JSON y guardar en una lista
            data_list = [json.loads(element) for element in list_elements]

            # Eliminar elementos de la lista en Redis
            self.redis_client.ltrim('list', len(list_elements), -1)

            for data in data_list:
                if 'air_wellness' in data:
                    air_data_dict = {"air_wellness": data['air_wellness'], "id": data['id'], "time": data['time']}
                    air_data_list.append(air_data_dict)
                elif 'co2_wellness' in data:
                    co2_data_dict = {"co2_wellness": data['co2_wellness'], "id": data['id'], "time": data['time']}
                    co2_data_list.append(co2_data_dict)
            if 'air_wellness' in data:
                air_data_mean = statistics.mean([data['air_wellness'] for data in air_data_list])
            elif 'co2_wellness' in data:
                co2_data_mean = statistics.mean([data['co2_wellness'] for data in co2_data_list])
            first_time = data_list[0]['time']

            print("\rDatos de aire:", air_data_list)
            print("\rDatos de CO2:", co2_data_list)

            queue_name = min(self.rabbitmq.queue_names, key=lambda x: self.rabbitmq.channel.queue_declare(queue=x, passive=True).method.message_count)
            print("queue_name:", queue_name)
            #self.rabbitmq.publish_data(queue_name, json.dumps(air_data_dict, ensure_ascii=False))
            #self.rabbitmq.publish_data(queue_name, json.dumps(air_data_dict, ensure_ascii=False))
            self.rabbitmq.publish_data(queue_name, json.dumps({"air_data_mean": air_data_mean, "co2_data_mean": co2_data_mean, "time": first_time}, ensure_ascii=False))


        else:
            print("\rNo hay datos en Redis")


class RabbitMQ:
    def __init__(self, rabbitmq_host, rabbitmq_port, queue_names):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.queue_names = queue_names
        for queue_name in queue_names:
            self.channel.queue_declare(queue=queue_name)

    def publish_data(self, queue_name, data):
        # Publicar datos en RabbitMQ
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=data)


class RedisDataProxyWithRabbitMQ(IData):
    def __init__(self, redis_data, rabbitmq):
        self.redis_data = redis_data
        self.rabbitmq = rabbitmq

    def process_data(self):
        self.redis_data.process_data()


def main():
    num_queues = int(sys.argv[1])

    # Crear una lista de nombres de colas dinámicamente
    rabbitmq_queue_names = [f'sensor_data_{i}' for i in range(1, num_queues+1)]
    print ("rabbitmq_queue_names:", rabbitmq_queue_names)
    window_size = 10  # Tamaño de la ventana
    redis_data = RedisData('localhost', 6379, window_size)
    rabbitmq = RabbitMQ('localhost', 5672, rabbitmq_queue_names)
    redis_data.rabbitmq = rabbitmq  # asignar objeto rabbitmq a redis_data
    redis_data_proxy_with_rabbitmq = RedisDataProxyWithRabbitMQ(redis_data, rabbitmq)

    while True:
        redis_data_proxy_with_rabbitmq.process_data()
        time.sleep(10)

if __name__ == '__main__':
    main()
