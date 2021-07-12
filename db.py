# 存储模块
import redis
import random
from error import PoolEmptyError
import setting


MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

REDIS_HOST = setting.HOST
REDIS_PORT = setting.PORT
REDIS_KEY = 'proxies1'

class RedisClient():

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        """
        建立redis连接
        :param host:
        :param port:
        """
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置初始化分数
        :param proxy:
        :param score:
        :return:增加的代理个数
        """
        if not self.db.zscore(REDIS_KEY,proxy):
            mapping = {proxy: score}
            return self.db.zadd(REDIS_KEY, mapping)

    def random(self):
        """
        随机获取有效代理
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return random.choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return random.choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        通过测试更新分数
        :param proxy:
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        score = int(score)
        if score > MIN_SCORE:
            print('代理',proxy,'当前分数', score-1)
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy)==None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy:
        :return:
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        mapping = {proxy: MAX_SCORE}
        return self.db.zadd(REDIS_KEY, mapping)

    def count(self):
        """
        获取代理个数
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
