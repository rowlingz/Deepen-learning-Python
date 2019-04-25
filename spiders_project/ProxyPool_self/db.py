# -*- coding:utf-8 -*-
import redis
from random import choice

# 默认参数
from setting import REDIS_KEY, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from setting import INITIAL_SCORE, MIN_SCORE, MAX_SCORE


class RedisClient:
    """
    创建一个存储模块，借助redis中有序集合构造代理池，储存代理及对应分数
    """
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化，建立连接
        :param host: redis地址
        :param port: redis端口
        :param password: redis密码
        """
        # decode_responses参数设置为true，写入的value值为str，否则为字节型
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        给代理池添加新代理，如果当前代理不存在代理池，则往代理池添加一个，分数为初始值
        :param proxy:新代理
        :param score: 初始分数值
        :return:向代理池添加新代理
        """
        if not self.exists(proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有序代理，首先尝试获取最高分代理，不存在则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)

        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                error = " 当前代理池无可用代理"
                print(error)
                raise error

    def decrease(self, proxy):
        """
        代理值减一分，分数低于最低值时，移除该代理
        :param proxy:
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1;')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除.')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy:
        :return: True--该代理存在，False--该代理不存在
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        return score is not None

    def max(self, proxy):
        """
        将可用代理分数值设为MAX_SCORE
        :param proxy:
        :return: 可用代理分数设为MAX_SCORE
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        返回集合的成员数
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """返回代理池当前所有可用代理"""
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

