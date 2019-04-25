# -*- coding:utf-8 -*-
import requests
from setting import PROXY_POOL_URL


def get_proxy():
    try:
        resp = requests.get(PROXY_POOL_URL)
        if resp.status_code == 200:
            return resp.text
    except ConnectionError:
        return None


if __name__ == '__main__':
    proxy = get_proxy()
    print(proxy)
    print(1)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except ConnectionError as e:
        print('Error', e.args)

