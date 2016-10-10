#!/usr/bin/env python
# encoding: utf-8


import http_config as config
import random
import urllib
import urllib2


TRY_TIME = 3


######################################################################
#
#                          HTTP(s)  Method
#
######################################################################
#
# GET Method
#
def http_get_method(url, time_out=5, user_agent=None, referer=None,
                    x_forwarded_for=None, accept_language=None):
    try_time = 0
    header = forge_headers(referer=referer, user_agent=user_agent,
                           x_forwarded_for=x_forwarded_for, accept_language=accept_language)
    while True:
        try:
            req = urllib2.Request(url, headers=header)
            res = urllib2.urlopen(req, timeout=time_out)
            content = res.read()
            return content
        except:
            try_time += 1
            if try_time > TRY_TIME:
                return None


#
# POST Method
#
def http_post_method(url, data=None, timeout=10):
    try_time = 0
    header = forge_headers(referer=url)
    while True:
        try:
            req = urllib2.Request(url, headers=header, data=urllib.urlencode(data))
            res = urllib2.urlopen(req, timeout=timeout)
            content = res.read()
            return content
        except:
            try_time += 1
            if try_time > TRY_TIME:
                return None


######################################################################
#
#                              Headers
#
######################################################################
#
# 伪造 User-Agent
#
def forge_user_agent():
    return random.choice(config.USER_AGENTS)


#
# 伪造 X-Forwarded-For
#
def forge_x_forwarded_for():
    return '%d.%d.%d.%d' % (random.randint(1, 254), random.randint(1, 254),
                            random.randint(1, 254), random.randint(1, 254))


#
# 伪造 Accept-Language
#
def forge_accept_language():
    return random.choice(config.Accept_Language)


#
# 伪造 Headers
#
def forge_headers(user_agent=None, referer=None, x_forwarded_for=None,
                  accept_language=None):
    headers = {}

    if user_agent == 'forge':
        headers['User-Agent'] = forge_user_agent()
    elif user_agent is not None:
        headers['User-Agent'] = user_agent
    else:
        pass

    if referer is not None:
        headers['Referer'] = referer

    if x_forwarded_for == 'forge':
        headers['X-Forwarded-For'] = forge_x_forwarded_for()
    elif x_forwarded_for is not None:
        headers['X-Forwarded-For'] = x_forwarded_for
    else:
        pass

    if accept_language == 'forge':
        # 这里强制使用简体中文,
        headers['Accept-Language'] = forge_accept_language()
    elif accept_language is not None:
        headers['Accept-Language'] = accept_language
    else:
        pass
    return headers
