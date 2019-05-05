# -*- coding:utf-8 -*-
"""
网页spider
"""
import requests
from lxml import html
from bs4 import BeautifulSoup
import time
import random


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
        for proxy in eval("self.{}()".format(callback)):
            print('成功获得到代理', proxy)
            yield proxy

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

    def crawl_xici(self):
        """新增西刺免费代理的获取"""
        xici_url = "https://www.xicidaili.com/nn"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/73.0.3683.103 Safari/537.36'
        }
        response = requests.get(xici_url, headers=headers)

        bf = BeautifulSoup(response.text, 'html.parser')
        pages = bf.find('div', class_='pagination')
        pages_total = pages.find_all('a')[-2].string
        for i in range(1, 100):      # 爬取5500条时被封，每页包含100个，
            url = "https://www.xicidaili.com/nn" + '/' + str(i)
            bf = None
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    bf = BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException:
                continue
            if bf:
                ip_table = bf.find('table')
                ip_list = ip_table.find_all('tr')
                for ip in ip_list[1:]:
                    ip_td = ip.find_all('td')
                    ip_url = ip_td[1].string
                    ip_port = ip_td[2].string
                    ip_type = ip_td[5].string
                    proxy = ':'.join([ip_url, ip_port])
                    yield proxy
                time.sleep(random.uniform(0.1, 3))
