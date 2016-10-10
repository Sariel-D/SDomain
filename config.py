#!/usr/bin/env python
# encoding: utf-8


######################################################################
#
#                              Dns
#
######################################################################
#
# dns查询设置
#
default_dns_setting = {
    'nameservers': ['114.114.114.114', '8.8.8.8'],
    'timeout': 5.0,  # @type: float | @value: 5s
}

#
# 过滤IP相关查询网站
#
ip_white_list = [
    'ip.911cha.com',
    'ip.293.net',
    'ip.xpcha.com',
    'www.ip138.com'
]

#
# 过滤dns相关查询网站
#
dns_white_list = [
    'dnspod.net',
    'dnsv3.com',
    'dnsv2.com',
    'xinnet.com',
    'hichina.com',
    '360safe.com',
    'iidns.com',
]


######################################################################
#
#                             Spider
#
######################################################################
#
#
# 被抓取的信息太多时候会造成卡顿，甚至卡死
# 可能的解决方案是利用url多线程抓取，避免跳转
#
selenium_spider_setting = {
    'aizhan': {
        'base_url': "http://dns.aizhan.com/{key_word}/{page}/",
        'begin_page': 1,
        'engine': 'phantomjs',
        'next_page_key': ">>",
        'next_page_style': 1,  # 1-> urllib | 2-> click
        'search_key': "//tr/td/a[1]",
        'search_max': 1000,
        'single_page_result_num': 20,
    },
    'baidu': {
        'base_url': "https://www.baidu.com/s?wd={key_word}&{param_key}={page}&ie=utf-8",
        'begin_page': 0,
        'engine': 'phantomjs',
        'next_page_key': "下一页",
        'next_page_style': 1,  # 1-> urllib | 2-> click
        'page_param': r"pn=\d+",
        'page_param_key': "pn",
        'search_key': "//a[@target='_blank'][@class='c-showurl']",
        'search_max': 1000,
        'single_page_result_num': 10,
    },
    'bing': {
        'base_url': "https://www.bing.com/search?q={key_word}&PC=U316&{param_key}={page}&FORM=PERE",
        'begin_page': 0,
        'browser': 'CHROME',  # PERE | CHROME
        'engine': 'phantomjs',
        'next_page_key': "//a[@class='sb_pagN']",
        'next_page_style': 1,  # 1-> urllib | 2-> click
        'page_param': r"first=\d+",
        'page_param_key': "first",
        'search_key': "//h2/a[@target='_blank']",
        'search_max': 1000,
        'single_page_result_num': 10,
    },
    'google': {
        'base_url': "https://www.google.com/#q={key_word}&{param_key}={page}",
        'begin_page': 0,
        'engine': 'phantomjs',
        'next_page_key': "下一页",
        'next_page_style': 2,  # 1-> urllib | 2-> click
        'page_param': r"start=\d+",
        'page_param_key': 'start',
        'search_key': "cite",
        'search_max': 1000,
        'single_page_result_num': 10,
    },
}

# 各自的try_time , 最后发送到http
slsubdomain_spider_setting = {
    'alexa': {
        'base_url': 'http://alexa.chinaz.com/default.aspx?domain=',
        'rule': r'\w*\.',  # + domain ---后面需要加域名匹配, 正则...不会的后果
        'time_out': 5,
        # headers
        'accept_language': None,
        'referer': 'forge',
        'user_agent': 'forge',
        'x_forwarded_for': None,
    },
    'links': {
        'base_url': 'http://i.links.cn/subdomain/?domain=',
        'rule': r'(?<=value="http://).*?(?=">)',  # https的匹配不到 ---不过还没见到过这种结果
        'time_out': 20,
        # headers
        'accept_language': None,
        'referer': 'forge',
        'user_agent': 'forge',
        'x_forwarded_for': None,
    },
    'netcraft': {
        'all_num_key': r'(?<=Found )\d*(?= sites)',
        'base_url': 'http://searchdns.netcraft.com/?host=',
        'rule': r'(?<=href="http://).*?(?=/")',
        'single_page_result_num': 20,
        'start_page': 1,
        'time_out': 10,
        # page
        'next_page_key': 'Next page',
        # headers
        'accept_language': None,
        'referer': 'forge',
        'user_agent': 'forge',
        'x_forwarded_for': None,
    },
    'sitedossier': {
        # spider
        'all_num_key': r'(?<=out of a total of )[,0-9]*(?=</i>)',
        'base_url': 'http://www.sitedossier.com/parentdomain/',
        'rule': r'(?<=http://).*?(?=/</a)',
        'single_page_result_num': 100,
        'start_page': 1,
        'time_out': 5,
        # page
        'next_page_key': 'Show next',  # Show remaining XX items
        'end_page_key': 'End of list',  # End of list.
        # headers
        'accept_language': None,
        'referer': 'forge',
        'user_agent': 'forge',
        'x_forwarded_for': None,
    }
}
