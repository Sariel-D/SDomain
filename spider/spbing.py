#!/usr/bin/env python
# encoding: utf-8


from network.ipv4 import check_ip_bind, check_host_complete
from selenium.webdriver.common.by import By
from spspider import Spider
import config
import re
import urllib2


domains = {}


#
# 必应每个页面共10个结果, 结果总数一般在第三个页面才可见, 第一个页面总显示 57,000,000
# bing 必须采用 https://www.bing.com 否则会自动跳转 http://cn.bing.com, 后者查询 IP 有问题
#
# 基于selenium
class BingSpider(Spider):
    def __init__(self, key=None, value=None):
        Spider.__init__(self)
        self.base_url = config.selenium_spider_setting['bing']['base_url']
        self.browser = config.selenium_spider_setting['bing']['browser']
        self.engine = config.selenium_spider_setting['bing']['engine']
        self.next_page_key = config.selenium_spider_setting['bing']['next_page_key']
        self.page = config.selenium_spider_setting['bing']['begin_page']
        self.page_max = config.selenium_spider_setting['bing']['single_page_result_num']
        self.page_param = config.selenium_spider_setting['bing']['page_param']
        self.page_param_key = config.selenium_spider_setting['bing']['page_param_key']
        self.search_key = config.selenium_spider_setting['bing']['search_key']
        self.search_max = config.selenium_spider_setting['bing']['search_max']
        self.next_page_style = config.selenium_spider_setting['bing']['next_page_style']
        self.key = key
        self.value = value
        self.key_word = key + ':' + value
        self.set_driver()

    def next_page(self):
        if self.next_page_style == 1:
            next_page = int(re.findall(self.page_param, self.url)[0].split('=')[1]) + self.page_max
            next_link, num = re.subn(self.page_param, self.page_param_key + '=' + str(next_page), self.url)
            self.open_url(next_link)
            self.page = next_page
            self.url = next_link
        elif self.next_page_style == 2:
            self.driver.find_element(By.XPATH, self.next_page_key).click()
            self.url = self.driver.current_url

    def find_next_button(self):
        try:
            self.driver.find_element(By.XPATH, self.next_page_key)
        except:
            return False
        return True

    def get_domain(self):
        info = self.driver.find_elements(By.XPATH, self.search_key)
        for i in info:
            link = i.get_attribute('href')
            try:
                proto, rest = urllib2.splittype(link)
                host, rest = urllib2.splithost(rest)
                host, port = urllib2.splitport(host)
                if port is None:
                    port = 80
                if host not in domains:
                    if self.key == 'ip':
                        if check_ip_bind(host, self.value):
                            domains[host] = port
                    elif self.key == 'domain':
                        host = check_host_complete(host, self.value)
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

    def __del__(self):
        if self.next_page_style == 2:
            self.driver.quit()


def bing_scan(key, value):
    sp = BingSpider(key=key, value=value)
    sp.get_info()
    return domains


if __name__ == '__main__':
    print bing_scan('ip', '173.208.209.155')
    print bing_scan('domain', 'baidu.com')
