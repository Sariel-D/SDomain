#!/usr/bin/env python
# encoding: utf-8


from network.ipv4 import check_ip_bind, check_host_complete
from selenium.webdriver.common.by import By
from spspider import Spider
import config
import urllib2


domains = {}


# 基于selenium
class GoogleSpider(Spider):
    def __init__(self, key=None, value=None):
        Spider.__init__(self)
        self.base_url = config.selenium_spider_setting['google']['base_url']
        self.engine = config.selenium_spider_setting['google']['engine']
        self.page = config.selenium_spider_setting['google']['begin_page']
        self.page_max = config.selenium_spider_setting['google']['single_page_result_num']
        self.page_param = config.selenium_spider_setting['google']['page_param']
        self.page_param_key = config.selenium_spider_setting['google']['page_param_key']
        self.search_key = config.selenium_spider_setting['google']['search_key']
        self.search_max = config.selenium_spider_setting['google']['search_max']
        self.next_page_key = config.selenium_spider_setting['google']['next_page_key']
        self.next_page_style = config.selenium_spider_setting['google']['next_page_style']
        self.key = key
        self.value = value
        self.key_word = key + ':' + value
        self.set_driver()

    def get_domain(self):
        info = self.driver.find_elements(By.TAG_NAME, self.search_key)
        for i in info:
            link = i.text.split('/')[0]
            if link == 'https:':
                link = i.text.split('/')[2]
            try:
                host, port = urllib2.splitport(link)
                if port is None:
                    port = 80
                if host not in domains:
                    if self.key == 'ip':
                        if check_ip_bind(host, self.value):
                            domains[host] = port
                    elif self.key == 'site':
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


def google_scan(key, value):
    sp = GoogleSpider(key=key, value=value)
    sp.get_info()
    return domains


if __name__ == '__main__':
    print google_scan('site', 'baidu.com')
    print google_scan('ip', 'baidu.com')
