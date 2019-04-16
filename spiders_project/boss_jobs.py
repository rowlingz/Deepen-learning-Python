# -*- coding:utf-8 -*-
# 借助boss直聘网站练习selenium, 网页登录等操作


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ChromeOptions
import json, csv
import time
import random


def inquire_job(browser, job_name):
    # 输入需要查询的职位
    input_string = browser.find_element_by_css_selector('.ipt-search')
    input_string.send_keys(job_name)

    button = browser.find_element_by_class_name('btn')
    button.click()


def get_job_items(browser):
    # 解析当前页面职位
    items = browser.find_elements_by_xpath("//div[@class='job-list']//li")

    file = open('boss_job_items.csv', 'a', encoding='utf-8')
    fieldnames = ['job_title', 'job_url', 'salary', 'condition', 'company_title', 'company_url',
                 'company_info', 'publis_name']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    for item in items:
        result = {}
        job = item.find_element_by_class_name('info-primary')
        result['job_title'] = job.find_element_by_class_name('job-title').text
        result['job_url'] = job.find_element_by_css_selector('a').get_attribute('href')
        result['salary'] = job.find_element_by_class_name('red').text
        result['condition'] = job.find_element_by_css_selector('p').text
        # '杭州 下城区 朝晖1-3年大专'
        company = item.find_element_by_class_name('info-company')
        result['company_title'] = company.find_element_by_css_selector('a').text
        result['company_url'] = company.find_element_by_css_selector('a').get_attribute('href')
        result['company_info'] = company.find_element_by_css_selector('p').text

        publis = item.find_element_by_class_name('info-publis')
        result['publis_name'] = publis.find_element_by_class_name('name').text

        writer.writerow(result)

    file.close()


def save_to_json(results):
    with open('boss_job_items.json', 'a', encoding='utf-8') as file:
        file.write(json.dumps(results, ensure_ascii=False))


def get_next_page(browser):
    # 翻页操作
    try:
        pages = browser.find_element_by_class_name('page')
        next_page_url = pages.find_element_by_class_name('next').get_attribute('href')
        print(next_page_url)
        return next_page_url
    except NoSuchElementException:
        raise NoSuchElementException


def main(job_name):
    with open('boss_cookies.json', 'r') as file:
        data = file.read()
        cookies = json.loads(data)

    # 避免被识别出为模拟浏览器
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    browser.get('https://www.zhipin.com/')
    for i in cookies:
        browser.add_cookie(i)
    browser.refresh()

    while True:
        try:
            inquire_job(browser, job_name)
            time.sleep(1)
            get_job_items(browser)
            # save_to_json(results)
            next_page_url = get_next_page(browser)
            time.sleep(random.uniform(1, 10))
            browser.get(next_page_url)
        except Exception:
            break

    browser.close()


# # 跳到了登陆页面
# login_url = 'https://signup.zhipin.com/?ka=header-register'
#
#
# # 保存cookies
# cookies = ''
# with open('boss_cookies.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(cookies))


if __name__ == '__main__':
    start_time = time.time()
    main('python爬虫')
    end_time = time.time()
    print(end_time - start_time)
