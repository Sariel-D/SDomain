#!/usr/bin/env python
# encoding: utf-8


from network.ipv4 import check_ip_bind
from selenium.webdriver.common.by import By
from spspider import Spider
import config
import urllib2


domains = {}


#
# 爱站中间一列 '标题'是爱站从新访问后刷新的, 容易卡死和502
#
# 基于selenium
class AizhanSpider(Spider):
    def __init__(self, value):
        Spider.__init__(self)
        self.base_url = config.selenium_spider_setting['aizhan']['base_url']
        self.engine = config.selenium_spider_setting['aizhan']['engine']
        self.page = config.selenium_spider_setting['aizhan']['begin_page']
        self.page_max = config.selenium_spider_setting['aizhan']['single_page_result_num']
        self.search_key = config.selenium_spider_setting['aizhan']['search_key']
        self.search_max = config.selenium_spider_setting['aizhan']['search_max']
        self.next_page_key = config.selenium_spider_setting['aizhan']['next_page_key']
        self.next_page_style = config.selenium_spider_setting['aizhan']['next_page_style']
        self.value = value
        self.key_word = value
        self.set_driver()

    def next_page(self):
        if self.next_page_style == 1:
            url = self.driver.current_url.split('/')
            next_page = int(url[-2]) + 1
            next_link = url[0] + '/' + url[2] + '/' + url[3] + '/' + str(next_page) + '/'
            self.open_url(next_link)
            self.page = next_page
            self.url = next_link
        elif self.next_page_style == 2:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.next_page_key).click()
            self.url = self.driver.current_url

    def find_next_button(self):
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, self.next_page_key)
        except:
            return False
        return True

    def check_max(self):
        try:
            url = self.driver.current_url
            result_num = int(url.split('/')[-2]) * self.page_max
            if result_num > self.search_max:
                # Overflow
                return True
        except:
            pass
        return False

    def get_domain(self):
        info = self.driver.find_elements(By.XPATH, self.search_key)
        for i in info:
            link = i.get_attribute('href')
            if link is None:
                continue
            try:
                proto, rest = urllib2.splittype(link)
                host, rest = urllib2.splithost(rest)
                host, port = urllib2.splitport(host)
                if port is None:
                    port = 80
                if host not in domains:
                    if check_ip_bind(host, self.value):
                        domains[host] = port
            except:
                pass

    def get_info(self):
        self.start_search()
        while True:
            self.get_domain()
            if self.check_max():
                break
            if not self.find_next_button():
                break
            self.next_page()


def aizhan_scan(value):
    sp = AizhanSpider(value)
    sp.get_info()
    return domains


if __name__ == '__main__':
    print aizhan_scan('173.208.209.155')
