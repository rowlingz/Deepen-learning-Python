# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import json


class ZhihuSpider:
    def __init__(self):
        """初始化变量"""
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36'
        }
        self.session = requests.Session()

    def add_cookies(self, cookies_file):
        """增加cookies"""
        with open(cookies_file, 'r') as file:
            cookies_json = json.loads(file.read())

        jar = requests.cookies.RequestsCookieJar()
        for dic_i in cookies_json:
            jar.set(dic_i['name'], dic_i['value'])
        self.session.cookies.update(jar)

    def web_link(self, url='https://www.zhihu.com/hot'):
        """网页连接"""
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                return None
        except requests.RequestException:
            return None

    def hot_items(self, hot_rep):
        """解析热榜上的top50话题"""
        bf = BeautifulSoup(hot_rep.text, 'html.parser')
        if bf:
            hot_items = bf.find_all('section', class_='HotItem')
            item_message = {}
            for hot_item in hot_items:

                item_message['index'] = hot_item.find('div', class_='HotItem-rank').string
                item_message['title'] = hot_item.find(class_='HotItem-title').string

                hot_item_content = hot_item.find('div', class_='HotItem-content')
                item_message['url'] = hot_item_content.a.attrs['href']
                item_message['id'] = item_message['url'].split('/')[-1]
                excerpt = hot_item_content.find('p', class_='HotItem-excerpt')
                if excerpt:
                    item_message['excerpt'] = excerpt.string
                else:
                    item_message['excerpt'] = None
                metrics = hot_item_content.find('div', class_='HotItem-metrics').get_text()
                item_message['hot'] = re.search(r"\d+", metrics).group()
                yield item_message

    def answers_to_item(self, item, offsets=10):
        """指定话题的回答收集"""
        item_id = item['id']
        answers = []
        for offset in range(offsets):
            url = 'https://www.zhihu.com/api/v4/questions/' + str(item_id) + \
                  '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2' \
                  'Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed' \
                  'by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2' \
                  'Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2' \
                  'Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2' \
                  'Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2' \
                  'A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&' \
                  'limit=5&offset=' + str(offset * 5) + '&platform=desktop&sort_by=default'
            item_rep = self.web_link(url)
            if item_rep:
                answer = item_rep.json()
                answers.extend(answer['data'])
            else:
                break
        return answers


def login_page(username, password):
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=options)
    home_url = 'https://www.zhihu.com/hot'
    login_url = 'https://www.zhihu.com/signin?next=%2Fhot'
    browser.get(home_url)
    url = browser.current_url
    if url == login_url:
        # 需要登录操作
        username_input = browser.find_element_by_xpath("//div[@class='SignFlow-account']//input[@class='Input']")
        username_input.send_keys(username)
        password_input = browser.find_element_by_xpath("//div[@class='SignFlow-password']//input[@class='Input']")
        password_input.send_keys(password)
        button = browser.find_element_by_xpath("//button[@type='submit']")
        button.click()
        if browser.current_url == home_url:
            # 表明登录成功
            cookies = browser.get_cookies()
            with open('zhihu_cookies.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(cookies))
            browser.quit()


if __name__ == '__main__':
    hot_zhihu = ZhihuSpider()
    hot_zhihu.add_cookies('zhihu_cookies.json')
    response = hot_zhihu.web_link()
    count = 0
    for hot_item in hot_zhihu.hot_items(response):
        print(hot_item)
        count += 1
        if count == 2:
            answers = hot_zhihu.answers_to_item(hot_item, 2)
            print(answers)
        if count > 4:
            break


