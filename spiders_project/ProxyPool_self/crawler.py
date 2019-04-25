# -*- coding:utf-8 -*-
"""
网页spider
"""
import requests
from lxml import html


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获得到代理', proxy)
            proxies.append(proxy)
        print(len(proxies))
        return proxies

    def crawl_shenji(self):
        shenji_url = "http://www.shenjidaili.com/open/"
        response = requests.get(shenji_url)
        etree = html.etree
        html_text = etree.HTML(response.text)

        https_1 = html_text.xpath("//div[@id='pills-stable_https']//td[1]/text()")[1:]
        https_2 = html_text.xpath("//div[@id='pills-gaoni_https']//td[1]/text()")[1:]
        http_1 = html_text.xpath("//div[@id='pills-stable_http']//td[1]/text()")[1:]
        http_2 = html_text.xpath("//div[@id='pills-gaoni_http']//td[1]/text()")[1:]
        https_1.extend(https_2)
        https_1.extend(http_1)
        https_1.extend(http_2)
        for ip in https_1:
            yield ip

