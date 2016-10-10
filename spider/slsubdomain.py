#!/usr/bin/env python
# encoding: utf-8


from config import slsubdomain_spider_setting
from network import http
from slsubspider import Spider
import re


#
# alexa.chinaz.com
# 优点: 结果可在源码中读取, 格式简单
# 缺点: 没事就喜欢503, 有的网站没有结果(qq.com)
#
class AlexaSpider(Spider):
    def __init__(self, domain=None):
        Spider.__init__(self)
        self.url = slsubdomain_spider_setting['alexa']['base_url'] + domain
        self.time_out = slsubdomain_spider_setting['alexa']['time_out']
        self.rule = slsubdomain_spider_setting['alexa']['rule'] + domain
        self.accept_language = slsubdomain_spider_setting['alexa']['accept_language']
        self.referer = slsubdomain_spider_setting['alexa']['referer']
        self.user_agent = slsubdomain_spider_setting['alexa']['user_agent']
        self.x_forwarded_for = slsubdomain_spider_setting['alexa']['x_forwarded_for']

    def get_info(self):
        self.start_search()
        return self.get_domain()


def get_alexa_records(domain):
    try:
        alexa_records = AlexaSpider(domain)
        return alexa_records.get_info()
    except:
        print '[!] Activates Alexa Anti-Scraping. Please check...'
        return []


#
# 每次都是重新扫描, 源码可见结果
#
class LinksSpider(Spider):
    def __init__(self, domain=None):
        Spider.__init__(self)
        self.url = slsubdomain_spider_setting['links']['base_url'] + domain
        self.time_out = slsubdomain_spider_setting['links']['time_out']
        self.rule = slsubdomain_spider_setting['links']['rule']
        self.accept_language = slsubdomain_spider_setting['links']['accept_language']
        self.referer = slsubdomain_spider_setting['links']['referer']
        self.user_agent = slsubdomain_spider_setting['links']['user_agent']
        self.x_forwarded_for = slsubdomain_spider_setting['links']['x_forwarded_for']

    def get_info(self):
        self.start_search()
        return self.get_domain()


def get_links_records(domain):
    try:
        links_records = LinksSpider(domain)
        return links_records.get_info()
    except:
        print '[!] Activates Links Anti-Scraping. Please check...'
        return []


#
# 源码可见结果,
# 总数 -> Found 453 sites
#
class NetcraftSpider(Spider):
    def __init__(self, domain=None):
        Spider.__init__(self)
        self.page = slsubdomain_spider_setting['netcraft']['start_page']
        self.url = slsubdomain_spider_setting['netcraft']['base_url'] + domain
        self.all_num_key = slsubdomain_spider_setting['netcraft']['all_num_key']
        self.time_out = slsubdomain_spider_setting['netcraft']['time_out']
        self.rule = slsubdomain_spider_setting['netcraft']['rule']
        self.single_page_result_num = slsubdomain_spider_setting['netcraft']['single_page_result_num']
        self.accept_language = slsubdomain_spider_setting['netcraft']['accept_language']
        self.referer = slsubdomain_spider_setting['netcraft']['referer']
        self.user_agent = slsubdomain_spider_setting['netcraft']['user_agent']
        self.x_forwarded_for = slsubdomain_spider_setting['netcraft']['x_forwarded_for']
        # sign
        self.last_record = None

    def next_page(self):
        next_url = self.url + '&last=' + self.last_record + '&from=' +\
                   str(self.page * self.single_page_result_num + 1) + "&restriction=site%20contains&position="
        self.content = http.http_get_method(next_url, time_out=self.time_out, user_agent='forge', referer='forge')
        self.page += 1

    def get_info(self):
        domains = []
        self.start_search()
        self.get_page_num()
        while self.page <= self.page_num:
            # domains.extend(self.get_domain())
            for single_domain in self.get_domain():
                if -1 == single_domain.find('netcraft'):
                    domains.append(single_domain)
            self.last_record = domains[-1]
            self.next_page()
        return domains


def get_netcraft_records(domain):
    try:
        netcraft_records = NetcraftSpider(domain)
        return netcraft_records.get_info()
    except:
        print '[!] Activates Netcraft Anti-Scraping. Please check...'
        return []


#
# 源码可见结果, 短时间多次访问会激活人机验证机制, 还可能被拉入黑名单
# 总数 -> Displaying items 1 to 100, out of a total of 268
#
class SitedossierSpider(Spider):
    def __init__(self, domain=None):
        Spider.__init__(self)
        self.page = slsubdomain_spider_setting['sitedossier']['start_page']
        self.url = slsubdomain_spider_setting['sitedossier']['base_url'] + domain
        self.all_num_key = slsubdomain_spider_setting['sitedossier']['all_num_key']
        self.time_out = slsubdomain_spider_setting['sitedossier']['time_out']
        self.rule = slsubdomain_spider_setting['sitedossier']['rule']
        self.single_page_result_num = slsubdomain_spider_setting['sitedossier']['single_page_result_num']
        self.accept_language = slsubdomain_spider_setting['sitedossier']['accept_language']
        self.referer = slsubdomain_spider_setting['sitedossier']['referer']
        self.user_agent = slsubdomain_spider_setting['sitedossier']['user_agent']
        self.x_forwarded_for = slsubdomain_spider_setting['sitedossier']['x_forwarded_for']

    def next_page(self):
        next_url = self.url + '/' + str(self.page * 100 + 1)
        self.content = http.http_get_method(next_url, time_out=self.time_out, user_agent='forge', referer='forge')
        self.page += 1

    def get_page_num(self):
        if self.all_num_key is not None:
            re_domain = re.compile(self.all_num_key)
            self.page_num = int(re_domain.findall(self.content)[0].replace(',', '')) / self.single_page_result_num + 1

    def get_info(self):
        domains = []
        self.start_search()
        self.get_page_num()
        while self.page <= self.page_num:
            domains.extend(self.get_domain())
            self.next_page()
        return domains


def get_sitedossier_records(domain):
    try:
        sitedossier_records = SitedossierSpider(domain)
        return sitedossier_records.get_info()
    except:
        print '[!] Activates Sitedossier Anti-Scraping. Please check...'
        return []
