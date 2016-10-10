#!/usr/bin/env python
# encoding: utf-8


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import quote
import re


#
# 此类包括以此生成的子类，都是以selenium模拟浏览器访问
#
class Spider:
    #
    # 初始化变量
    #
    def __init__(self, driver=None, engine=None, base_url="", next_page_key=None, page=None, page_max=None,page_param=None,
                 page_param_key=None, search_key=None, search_max=None, next_page_style=None, url=None,
                 key=None, value=None):
        self.driver = driver
        self.engine = engine
        # 以下变量必须设置
        self.base_url = base_url,
        self.next_page_key = next_page_key
        self.page = page
        self.page_max = page_max
        self.page_param = page_param
        self.page_param_key = page_param_key
        self.search_key = search_key
        self.search_max = search_max
        self.next_page_style = next_page_style
        self.url = url
        # 输入参数
        self.key = key
        self.value = value
        self.key_word = None

    #
    # 设置驱动浏览器，并直接开始访问
    #
    def set_driver(self):
        if self.engine.lower() == 'chrome':
            self.driver = webdriver.Chrome
        elif self.engine.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.engine.lower() == 'android':
            self.driver = webdriver.Android()
        elif self.engine.lower() == 'edge':
            self.driver = webdriver.Edge()
        else:
            self.driver = webdriver.PhantomJS()
        if (self.url != '') and (self.url is not None):
            self.open_url(url=self.url)

    #
    # 生成目标地址
    #
    def generate_link(self):
        return self.base_url.format(key_word=quote(self.key_word), param_key=self.page_param_key, page=self.page)

    #
    # 访问页面
    #
    def start_search(self):
        self.open_url(self.generate_link())

    def open_url(self, url):
        self.driver.get(url)
        self.url = url

    #
    # 翻页相关函数
    #
    def pervious_page(self):
        self.url = self.driver.current_url
        pass

    def next_page(self):
        if self.next_page_style == 1:
            next_page = int(re.findall(self.page_param, self.url)[0].split('=')[1]) + self.page_max
            next_link, num = re.subn(self.page_param, self.page_param_key + '=' + str(next_page), self.url)
            self.open_url(next_link)
            self.page = next_page
            self.url = next_link
        else:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.next_page_key).click()
            self.url = self.driver.current_url

    def find_next_button(self):
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.next_page_key)
        except:
            return False
        return True

    #
    # 检查是否超过最大查询数量
    #
    def check_max(self):
        try:
            self.url = self.driver.current_url
            search_num = int(re.findall(self.page_param, self.url)[0].split('=')[1]) + self.page_max
            if search_num > self.search_max:
                # Overflow
                return True
        except:
            pass
        return False

    #
    # 抓取 域名|IP
    #
    def get_domain(self):
        pass

    def parse_page(self):
        bs = BeautifulSoup(self.driver.page_source, 'html5lib')
        # 处理bs代码

    #
    #   抓取入口
    #
    def get_info(self):
        pass


    # 手动激活del
    def __del__(self):
        self.driver.quit()
        pass
