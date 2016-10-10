#!/usr/bin/env python
# encoding: utf-8


from network import http
import re


#
# 此类包括以此生成的子类，都是直接访问页面正则匹配
#
class Spider:
    def __init__(self):
        # 重要
        self.all_num_key = None
        self.time_out = None
        self.rule = None
        self.single_page_result_num = None
        self.url = None
        # headers
        self.accept_language = None
        self.referer = None
        self.user_agent = None
        self.x_forwarded_for = None
        # 产生
        self.content = None
        self.page_num = None

    def start_search(self):
        self.content = http.http_get_method(self.url, time_out=self.time_out, user_agent=self.user_agent,
                                            referer=self.referer, accept_language=self.accept_language,
                                            x_forwarded_for=self.x_forwarded_for)

    def get_page_num(self):
        if self.all_num_key is not None:
            re_domain = re.compile(self.all_num_key)
            self.page_num = int(re_domain.findall(self.content)[0]) / self.single_page_result_num + 1

    def next_page(self):
        pass

    def get_domain(self):
        re_domain = re.compile(self.rule)
        return re_domain.findall(self.content)

    # 入口
    def get_info(self):
        pass
