#!/usr/bin/env python
# encoding: utf-8


import re
import socket
import struct
import urllib

######################################################################
#
#                              Domain
#
######################################################################
#
# 检查域名和IP是否绑定
#
def check_ip_bind(domain, target_ip):
    ip = get_ip_by_hostname(domain)
    if ip is None:
        return False
    elif ip != target_ip:
            return False
    return True


#
# 通过主机名获取ip
#
def get_ip_by_hostname(hostname):
    try_time = 0
    while True:
        try:
            # ip -> (2, 1, 6, '', ('115.29.202.62', 80))
            ip = socket.getaddrinfo(hostname, 'http')[0][4][0]
            return ip
        except:
            try_time += 1
            if try_time >= 3:
                return None


#
# ip反查询域名
#
def get_hostname_by_ip(ip):
    pass


#
#  正则匹配ip, 返回list
#
def matching_ip(text):
    ip = []
    re_ip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    for single_ip in re_ip.findall(text):
        ip.append(single_ip)
    return ip


#
# 检查域名是否完整, 不完整则尝试补充
#
def check_host_complete(host, hostname):
    host = host.rstrip().rstrip('.')
    host_list = host.split('.')
    hostname_list = hostname.split('.')
    # 网站存活
    try:
        status = urllib.urlopen('http://' + host).code
    except:
        status = -1
    if status == 200:
        pass
    # 仅有二级域名且完整
    elif hostname == host:
        pass
    # 二级域名可以找到
    elif hostname_list[0] in host_list:
        index = host_list.index(hostname_list[0])
        if index:
            host_list = host_list[0:index]
            host_list.extend(hostname_list)
            host = '.'.join(host_list)
        else:
            # 顶级域名不完整
            host = hostname
    elif host_list[-1] not in hostname_list[0]:
        # 三级以上域名不完整, 无法得到真正地址, 尝试补充域名
        host_list.extend(hostname_list)
        host = '.'.join(host_list)
    else:
        # 二级域名不完整 | 可能三级域名等都不完整
        host_list = host_list[:-1]
        host_list.extend(hostname_list)
        host = '.'.join(host_list)
    return host


######################################################################
#
#                               IP
#
######################################################################
#
# 将点分十进制转换为int
#
def ip_trans_int(ip_format):
    ip = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip_format)))[0])
    return ip


#
# 将int转化为点分十进制
#
def ip_trans_format(ip_int):
    ip = socket.inet_ntoa(struct.pack('I', socket.htonl(ip_int)))
    return ip


#
# 输出IP段内所有IP
#
def ip_filter(ips):
    ip_list = []
    if ips.find('/') != -1:
        base_filter = ips.split('/')
        base_format = ip_trans_int(base_filter[0])
        final_int = 2**(32 - int(base_filter[1]))
        base_int = (base_format >> 32 - int(base_filter[1]) << 32 - int(base_filter[1]))
        begin = base_int + 1
        end = base_int + final_int
        for ip_int in range(begin, end):
            ip_list.append(ip_trans_format(ip_int))
    else:
        ip_list.append(ips)
    return ip_list
