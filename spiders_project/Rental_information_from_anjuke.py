# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pymysql
import time
import pandas as pd
import random


def web_link(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36'
    }
    bf = None
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            bf = BeautifulSoup(response.text, 'html.parser')
    except requests.ConnectionError as e:
        error = pd.DataFrame({'url': [url], 'error': [e]})
        error.to_csv('fail_url.csv', index=False, header=False, mode='a', encoding='utf_8_sig')
    return bf


def get_city_url(basic_url):
    """解析安居客不同城市的网址"""
    bf = web_link(basic_url)

    if bf:
        contents = bf.find_all('div', class_='city_list')
        city_message = {}

        for content in contents:
            citys = content.find_all('a')
            for city in citys:
                city_message['city_name'] = city.string
                city_message['city_url'] = city.get('href')
                yield city_message


def insert_city_url(conn, city_message):
    """将城市网址字典信息逐条插入数据库"""
    sql_insert = "insert into anjuke_citys_url (city_name, city_url) values (%(city_name)s, %(city_url)s)"
    sql_select = "select city_name from anjuke_citys_url where city_name=%s"

    cur = conn.cursor()
    try:
        cur.execute(sql_select, city_message['city_name'])
        result_num = cur.rowcount
        if result_num == 0:
            cur.execute(sql_insert, city_message)
            conn.commit()
    except Exception as e:
        print(city_message['name'], e)
    finally:
        cur.close()


def create_citys_url_table():
    """获取安居客所有城市的url,并存入库"""
    start_time = time.time()
    conn = pymysql.connect(host="localhost", user="root", password="root",
                           database="spider_projects", port=3306, charset="utf8")

    basic_url = "https://www.anjuke.com/sy-city.html"

    for city_info in get_city_url(basic_url):
        insert_city_url(conn, city_info)

    conn.close()

    end_time = time.time()
    print(end_time - start_time)
    print('end')


# 解析指定页面下的房源信息

# 1、url字符拼接
def get_price_area_items(hangzhou_url):
    """获取价格，户型的类别标签，后续进行url拼接"""
    second_hand_url = hangzhou_url + "/sale/"
    sub_bf = web_link(second_hand_url)

    groups = sub_bf.find_all('div', class_='items')

    prices = groups[1].find_all('a')
    price_items = {}
    for price in prices:
        price_items[price.string] = price.get('href').split('/')[-2]

    house_types = groups[3].find_all('a')
    house_type_items = {}
    for house_type in house_types:
        house_type_items[house_type.string] = house_type.get('href').split('/')[-2]

    return {'price_items': price_items, 'house_type_items': house_type_items}


# 创建条件url
def get_each_city_url(city_url, price_house_type):
    """获取特定条件下的url"""

    second_hand_url = city_url + "/sale/"
    sub_bf = web_link(second_hand_url)
    groups = sub_bf.find_all('div', class_='items')
    groups_num = len(groups)

    price_items = price_house_type['price_items']
    house_type_items = price_house_type['house_type_items']

    regions = groups[0].find_all('a')
    detail_info = {}
    for price_key in price_items:
        detail_info[price_key] = price_items[price_key]

        for type_key in house_type_items:
            detail_info[type_key] = house_type_items[type_key]
            com_values = house_type_items[type_key] + "-" + price_items[price_key] + "/"

            for region in regions:
                detail_info['region_name'] = region.string
                region_url = region.attrs['href']
                region_bf = web_link(region_url)

                sub_regions = region_bf.find('div', class_='sub-items')
                if sub_regions:
                    sub_regions = sub_regions.find_all('a')
                    for sub_region in sub_regions:
                        sub_url = sub_region.get('href')
                        detail_info['sub_name'] = sub_region.string
                        detail_info['detail_url'] = sub_url + com_values
                        yield detail_info
                else:
                    detail_info['sub_name'] = 'all'
                    sub_url = region_url
                    detail_info['detail_url'] = sub_url + com_values
                    yield detail_info

                time.sleep(random.uniform(0, 0.02))


# 3、解析指定条件下的房源信息
def get_all_info(url, conn):
    """获取指定类别url下所有页码的信息"""
    next_url = url
    while True:
        bf = web_link(next_url)

        # 解析当前url下的房源，如果没有符合条件的结果，退出程序
        try:
            filter_result = bf.find('ul', id='houselist-mod-new', class_='houselist-mod houselist-mod-new')
            house_list = filter_result.find_all('li', class_='list-item')
        except AttributeError:
            break
        else:
            # 解析全页数据，并存入数据库
            result = get_detail_info(house_list)
            if result:
                insert_house_info(conn, result)

        # 判断是否存在下一页，存在则作为下一个解析目标，否则退出
        try:
            pages = bf.find('div', class_='multi-page')
            next_url = pages.find('a', class_='aNxt').get('href')
        except AttributeError:
            break


# 3.1 获取全页数据
def get_detail_info(house_list):
    """解析每一页数据并进行数据录入"""
    result = []
    if not house_list:
        return result

    for house in house_list:
        house_message = {}
        house_message['title'] = house.find('div', class_='house-title').a.attrs['title']
        house_message['url'] = house.find('div', class_='house-title').a.get('href')

        details_item_feature = house.find('div', class_='details-item').find_all('span')

        house_message['house_type'] = details_item_feature[0].string
        house_message['area'] = details_item_feature[1].string
        house_message['floor'] = details_item_feature[2].string
        house_message['year'] = details_item_feature[3].string

        details_local = house.find_all('div', class_='details-item')[1].find('span')
        details_local = details_local.attrs['title'].split()
        house_message['community'] = details_local[0]
        house_message['address'] = details_local[1]

        tags = house.find('div', class_='tags-bottom')

        if tags:
            house_message['tags'] = ','.join([i.string for i in tags.find_all('span')])
        else:
            house_message['tags'] = ''

        house_message['price_det'] = house.find('span', class_='price-det').get_text()
        house_message['price_unit'] = house.find('span', class_='unit-price').string

        result.append(list(house_message.values()))
    return result


# 3.1.1 数据插入数据库
def insert_house_info(conn, result):
    """数据存入数据库"""
    field_name = ['title', 'url', 'house_type', 'area',
                  'floor', 'year', 'community', 'address', 'tags', 'price_det', 'price_unit']
    keys = ", ".join(field_name)
    qmark = ", ".join(["%s"] * len(field_name))
    sql = "INSERT INTO house_message_hz(%s) VALUES (%s)" % (keys, qmark)
    cur = conn.cursor()
    try:
        if len(result) > 1:
            cur.executemany(sql, result)
        else:
            cur.execute(sql, result)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()


def run(city_url):
    start_time = time.time()
    price_house_type = get_price_area_items(city_url)

    conn = pymysql.connect(host="localhost", user="root", password="root",
                           database="spider_projects", port=3306, charset="utf8")
    i = 0
    for city in get_each_city_url(city_url, price_house_type):
        url = city['detail_url']
        get_all_info(url, conn)
        time.sleep(random.uniform(0, 0.02))
        i += 1
        print(i)
        if i == 50:
            break

    end_time = time.time()
    print(end_time - start_time)
    print('end')


if __name__ == "__main__":

    hz_url = "https://hangzhou.anjuke.com"
    run(hz_url)

