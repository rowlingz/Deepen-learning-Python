# -*- coding:utf-8 -*-
from db import RedisClient
from crawler import Crawler

# 默认参数
from setting import POOL_UPPER_THRESHOLD


class Getter:
    """
    获取代理，加载至代理池中
    """
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """判断代理池是否达到限制"""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
    redis = getter.redis
    print(redis.count())
    print('end')

