# -*- coding:utf-8 -*-

import requests
from requests.exceptions import ConnectionError
from lxml import html


from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException

import pymysql
import time
import random


ProxyPool_url = "http://127.0.0.1:5000/random"


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.103 Safari/537.36'
}


class SpiderCSDN:
    """获取指定博主发布的全部文章，并录入数据录"""

    def get_proxy(self):
        """从代理池获取代理"""
        try:
            resp = requests.get(ProxyPool_url, headers=headers)
            if resp.status_code == 200:
                return resp.text
            else:
                return None
        except ConnectionError:
            return None

    def get_pages(self, user_id, proxy):
        """
        借助selenium获取页码总数
        """
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--proxy - server = https:// ' + proxy)
        browser = webdriver.Chrome(options=options)
        url = 'https://blog.csdn.net/' + user_id
        browser.get(url)
        end_page = 1
        try:
            pages = browser.find_elements_by_xpath("//li[@data-page]")
            if pages:
                end_page = pages[-1].text
                return end_page
        except NoSuchElementException:
            return end_page
        finally:
            browser.quit()
        return 1

    def single_page(self, proxy, user_id, page):
        """
        建立单页连接
        :param proxy: 当前可用代理
        :param user_id: 博主id
        :param page: 页码
        :return: 响应体
        """
        proxies = {
            'https': 'https://' + proxy,
            'http': 'http://' + proxy
        }
        page_url = "https://blog.csdn.net/{}/article/list/{}?".format(user_id, page)
        try:
            response = requests.get(page_url, headers=headers, proxies=proxies)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except ConnectionError:
            return None

    def get_comments(self, resp):
        """
        单页页面解析，获取已发表博客信息
        :param resp: 页码响应体
        :return: 博客信息， 生成器
        """
        etree = html.etree
        html_text = etree.HTML(resp)
        pages = html_text.xpath("//div[@class='article-list']/div[@class]")
        article = {}
        for page in pages[1:]:
            article['url'] = page.xpath("./h4/a/@href")[0]
            article['id'] = article['url'].split('/')[-1]
            article['title_type'] = page.xpath("./h4/a/text()")[0].strip()
            article['title'] = page.xpath("./h4/a/text()")[1].strip()
            article['content'] = page.xpath("./p/a/text()")[0].strip()
            article['publish_time'] = page.xpath("./div/p[1]/span/text()")[0]
            article['read_num'] = page.xpath(".//span[@class='num']/text()")[0]
            article['comment_num'] = page.xpath(".//span[@class='num']/text()")[1]
            yield article

    def save_article(self, coon, article):
        """
        将博客信息存入mysql数据库
        :param coon: 数据库连接
        :param article: 博客信息
        :return:
        """
        cur = coon.cursor()

        # 以博文的id为主键，如果存在则更新阅读数和评论数，不存在则新插入一条
        sql_insert = "INSERT INTO CSDN_articles" \
                     "(id, url, title_type, title, content, publish_time, read_num, comment_num) " \
                     "VALUES" \
                     " (%(id)s, %(url)s, %(title_type)s, %(title)s, %(content)s, %(publish_time)s, " \
                     "%(read_num)s, %(comment_num)s) " \
                     "ON DUPLICATE KEY UPDATE read_num=%(read_num)s, comment_num=%(comment_num)s"

        try:
            cur.execute(sql_insert, article)
            coon.commit()
            print('插入成功')
        except Exception:
            coon.rollback()
            print(article['url'], '插入失败')

    def start(self, user_id):
        """整个流程"""

        # 获取随机代理
        proxy = self.get_proxy()

        # 获取整个页码数
        pages = self.get_pages(user_id, proxy)

        coon = pymysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='root',
                               database='spider_projects',
                               charset='utf8')

        # 逐页获取信息
        for page in range(1, pages+1):

            resp = self.single_page(page, user_id, proxy)

            # 一旦来连接失败，更换代理后重新连接
            while resp is None:
                proxy = self.get_proxy()
                resp = self.single_page(page, user_id, proxy)

            # 获取当前页的所有文章
            for article in self.get_comments(resp):
                # 文章存入库
                # print(article)
                self.save_article(coon, article)
            time.sleep(random.uniform(0.01, 1))
        coon.close()


if __name__ == '__main__':
    my_CSDN = SpiderCSDN()
    my_id = 'weixin_40041218'
    my_CSDN.start(my_id)
    print('end')

