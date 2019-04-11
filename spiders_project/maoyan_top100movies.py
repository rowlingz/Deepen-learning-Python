# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import time
import json
import random
from lxml import html


def web_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html_text):
    etree = html.etree
    html_text = etree.HTML(html_text)
    items = html_text.xpath("//dd")
    for item in items:
        result = {}
        result['index'] = item.xpath("./i/text()")[0]
        result['img'] = item.xpath("./a/img[2]/@data-src")
        result['url'] = "https://maoyan.com" + item.xpath(".//p[@class='name']/a/@href")[0]
        result['title'] = item.xpath(".//p[@class='name']/a/@title")[0]
        result['actor'] = item.xpath(".//p[@class='star']/text()")[0].strip()
        result['time'] = item.xpath(".//p[@class='releasetime']/text()")[0]
        result['score'] = ''.join(item.xpath(".//p[@class='score']/i/text()"))
        yield result


def write_to_file(content):
    with open('maoyan_movie.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html_text = web_link(url)
    if html:
        for item in parse_one_page(html_text):
            write_to_file(item)


if __name__ == "__main__":
    for i in range(10):
        main(offset=i * 10)
        time.sleep(random.uniform(0, 0.5))
