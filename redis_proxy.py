import redis

class RedisProxy:
    def __init__(self, host="localhost", port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def get_data(self):
        pollution_data = self.redis_client.hgetall("pollution_data")
        meteo_data = self.redis_client.hgetall("meteo_data")
        print(meteo_data)
        return pollution_data

if __name__ == '__main__':
    redis_proxy = RedisProxy()
    data = redis_proxy.get_data()
    print(data)