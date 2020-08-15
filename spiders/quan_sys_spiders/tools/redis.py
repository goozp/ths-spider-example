import redis

from quan_sys_spiders.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class RedisClient(object):
    
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化连接
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        if password == 'None':
            self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)
        else:
            self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)


    def set_value(self, key, value, ex=None):
        return self.db.set(key, value, ex=None)

    def get_value(self, key):
        if self.db.exists(key):
            return self.db.get(key)
        else:
            return None

    def delete_value(self, key):
        return self.db.delete(key)
