# -*- coding:utf-8 -*-
import asyncio
import aiohttp
import time
from random import randint
from aiohttp import ClientError
import requests
from requests.exceptions import ConnectionError

from db import RedisClient

# 默认参数
from setting import TEST_URL, VALID_STATUS_CODES, BATCH_TEST_SIZE


class Tester:
    """检测代理池中代理是否可用，可用则分数至为100，否则分数减一"""
    def __init__(self):
        self.redis = RedisClient()

    async def single_test(self, proxy):
        """单个代理测试"""
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = "http://" + proxy
                print("正在测试：", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status_code in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print(proxy, '代理可用')
                    else:
                        self.redis.decrease(proxy)
                        print(proxy, 'IP 请求响应码不合法')
            except (ClientError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """异步测试"""
        print('开始测试代理')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')

            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                test_proxies = proxies[start: stop]
                tasks = [self.single_test(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(randint(1, 5))
        except Exception as e:
            print('测试器发生错误', e.args)


class Tester_2:
    def __init__(self):
        self.redis = RedisClient()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36'
        }

    def single_test(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            resp = requests.get(TEST_URL, proxies=proxies, headers=self.headers)
            if resp.status_code == 200:
                print(proxy, '代理可用')
                self.redis.max(proxy)
            else:
                self.redis.decrease(proxy)
                print(proxy, 'IP 请求响应码不合法')
        except ConnectionError:
            print('代理请求失败', proxy)
            self.redis.decrease(proxy)

    def run(self):
        count = self.redis.count()
        print('共有', count, '个代理')
        print('开始检测代理')
        proxies = self.redis.all()
        i = 0
        try:
            for proxy in proxies:
                print(proxy)
                i += 1
                self.single_test(proxy)
                time.sleep(randint(1, 5))
                if i == 15:
                    break
        except Exception as e:
            print('测试器发生错误', e)


if __name__ == '__main__':
    tester = Tester_2()
    tester.run()
