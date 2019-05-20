# -*- coding:utf-8 -*-
# 从生意参谋获取竞争市场中的入店来源数据


import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import WebDriverException, TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from pandas import DataFrame


def combin_url(timepoint, rivalUser1Id=None, rivalUser2Id=None):
    """生成指定条件下的url"""
    daterange = ''.join([timepoint, "%7C", timepoint])
    params = {
        "cateId": 50025705,
        "dateRange": daterange,
        "dateType": 'day',
        "parentCateId": 0,
        "rivalUser1Id": rivalUser1Id,
        "rivalUser2Id": rivalUser2Id
    }
    if params['rivalUser2Id'] is None:
        params.pop('rivalUser2Id')
    if params['rivalUser1Id'] is None:
        params.pop('rivalUser1Id')
    basic_url = "https://sycm.taobao.com/mc/ci/shop/analysis?cateFlag=1&"
    url = basic_url + '&'.join([key + "=" + str(value) for key, value in params.items()])
    return url


def bulid_link(login_url):
    """建立连接，并手动登录"""
    options = ChromeOptions()
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=options)
    browser.get(login_url)
    return browser


def wait_refresh(browser, url):
    """访问指定条件的页面"""
    browser.get(url)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    wait = WebDriverWait(browser, 20)
    try:
        kinds = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='sycm-mc-flow-analysis']//li[@class='oui-index-picker-item']")))
    except TimeoutException:
        time.sleep(5)
        kinds = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='sycm-mc-flow-analysis']//li[@class='oui-index-picker-item']")))


# 中间函数
def add_table(browser):
    # 点击加号，进行项目扩展
    try:
        table_adds = browser.find_elements_by_xpath("//span[contains(@class,'ant-table-row-collapsed')]")
        print(len(table_adds))
        for table_add in table_adds:
            table_add.click()
    except WebDriverException:
        print("当前无扩展对象")


def close_expand(browser):
    # 点击减号，项目收缩
    try:
        table_expandes = browser.find_elements_by_xpath("//span[contains(@class,'ant-table-row-expanded')]")
        print(len(table_expandes))
        for table_expande in table_expandes:
            table_expande.click()
    except WebDriverException:
        print("当前无收缩对象")


def click_option(browser, source_name):
    """更换按钮，获得其他条件的数据"""
    condition_statement = "//div[@id='sycm-mc-flow-analysis']//li/label//span[contains(text(),'{}')]/" \
                          "ancestor::label/span[contains(@class,'ant-radio')]".format(source_name)
    current = browser.find_element_by_xpath(condition_statement)
    current.click()
    button_class = current.get_attribute('class')
    print(button_class)
    while button_class != "ant-radio ant-radio-checked":
        time.sleep(0.5)
        button_class = current.get_attribute('class')
        print(source_name, button_class)
    print("按钮更换完成")
    time.sleep(2)


def get_datas(browser, source_name, timepoint):
    """获取每次子条件下的数据"""
    tables_total = browser.find_elements_by_xpath("//div[@id='sycm-mc-flow-analysis']//tbody/tr")
    print(len(tables_total))
    while len(tables_total) < 289:
        add_table(browser)
        close_expand(browser)
        tables_total = browser.find_elements_by_xpath("//div[@id='sycm-mc-flow-analysis']//tbody/tr")

    # 生成dataframe格式数据
    datas = [value.text.split('\n')[:4] for value in tables_total]
    total_datas = DataFrame(datas)

    # 添加时间列
    total_datas['data_time'] = [timepoint] * total_datas.shape[0]

    # 添加类别列
    total_datas['kinds'] = [source_name] * total_datas.shape[0]

    return total_datas


if __name__ == "__main__":
    store_dics = {
        '2962070462': '阿道夫梦卓专卖店',
        '217101303': '徽歌旗舰店'
    }

    time_list = list(map(lambda x: x.strftime("%Y-%m-%d"), pd.date_range('20190501', '20190515')))

    login_url = "https://sycm.taobao.com/custom/login.htm"

    # 建立连接并登录
    browser = bulid_link(login_url)

    store_id = list(store_dics.keys())
    # 解析指定id的数据
    rivalUser1Id = store_id.pop(0)
    rivalUser1name = store_dics[rivalUser1Id]
    rivalUser2Id = store_id.pop(0)
    rivalUser2name = store_dics[rivalUser2Id]

    filename = 'data_' + rivalUser1name + '_' + rivalUser2name + '.csv'
    csv_header = [['序号', '流量来源', 'sovya索薇娅旗舰店', rivalUser1name, rivalUser2name, 'date_time', 'kinds']]
    header_col = DataFrame(csv_header)
    header_col.to_csv(filename, header=False, encoding='utf_8_sig', index=False)

    for timepoint in time_list[:3]:
        item_url = combin_url(timepoint, rivalUser1Id, rivalUser2Id)
        wait_refresh(browser, item_url)

        sources = browser.find_elements_by_xpath("//div[@id='sycm-mc-flow-analysis']//li")
        numbers = len(sources)
        print(numbers)
        # 扩展二级目录
        for i in range(numbers):
            # 类别名
            source_name = sources[i].text
            print(source_name, "开始测试")

            # 更换按钮
            if i == 1:
                time.sleep(5)
            click_option(browser, source_name)

            # 获取所有数据并存储
            data_df = get_datas(browser, source_name, timepoint)
            print("开始获取数据")
            # 数据追加
            data_df.to_csv(filename, mode='a', header=False, encoding='utf_8_sig')
            print("数据追加完成")

