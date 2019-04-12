# -*- coding:utf-8 -*-
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re


def web_link(offset, keyword):
    """
    ajax网页连接，
    :param offset: ajax参数
    :param keyword: 搜索关键字
    :return: json
    """
    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36'
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None


def get_images(resp):
    """解析指定网页返回的json，查找image的url"""
    if resp:
        items = resp.get('data')
        for item in items:
            title = item.get('title')
            if title:
                # 有的标题含有特殊字符，无法组成文件名，用正则表达式进行替换
                title = re.sub(r'\\|\|', '', title)
                images = item.get('image_list')
                for image in images:
                    yield {
                        'title': title,
                        'image_url': image.get('url')
                    }


def save_image(item):
    """图片url保存至文件夹，按title分文件保存"""
    img_path = 'pictures' + os.path.sep + item.get('title')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    try:
        response = requests.get(item.get('image_url'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(img_path, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)

    except requests.RequestException:
        print('Failed to Save Image', item)


def get_all_images(offset, keyword="风景"):
    """下载图片的整个链路"""
    resp = web_link(offset, keyword)
    for item in get_images(resp):
        save_image(item)


if __name__ == "__main__":
    start_group = 0
    end_group = 5
    groups = [i * 20 for i in range(start_group, end_group+1)]
    pool = Pool()
    pool.map(get_all_images, groups)
    pool.close()
    pool.join()



