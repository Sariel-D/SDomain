#!/usr/bin/env python
# encoding: utf-8


from dnsdb.rfile import data_integration
from network.dns_func import *
from subdomain import get_subdomain
from optparse import OptionParser
import sys


options = OptionParser(usage='%prog domain [options]', description='Example: python %prog zonetransfer.me')
options.add_option('-f', '--file', type='string', default='', help='Dnsdb File')


# 以后有兄弟域名就在外面加个循环


def sdomain(target_domain, file=''):
    domains = {
                'dns': {
                    'a': [],
                    'ns': [],
                    'soa': [],
                    'mx': [],
                },
                'subdomain': {}
    }

    # 查询 A 记录
    print '[*] Starting A Search...'
    a_records = get_a_record(target_domain)
    for a_record in a_records['a']:
        domains['dns']['a'].append(a_record)

    # 查询 NS 记录, 同时检测域传送漏洞
    print '[*] Starting NS Search...'
    ns_records = get_ns_record(target_domain)
    domains['dns']['ns'] = ns_records['ns']
    if ns_records['zone_vul'] and (ns_records['zone_record'] is not None):
        for a_record in ns_records['zone_record']['a']:
            subdomain = a_record['service']
            domains['subdomain'][subdomain] = {'a': [], 'cname': []}

        for cname_record in ns_records['zone_record']['cname']:
            subdomain = cname_record['service']
            domains['subdomain'][subdomain] = {'a': [], 'cname': []}

        for a_record in ns_records['zone_record']['a']:
            subdomain = a_record['service']
            domains['subdomain'][subdomain]['a'].append(a_record['value'])

        for cname_record in ns_records['zone_record']['cname']:
            subdomain = cname_record['service']
            sub_a_record = get_a_record(subdomain)
            domains['subdomain'][subdomain]['a'].extend(sub_a_record['a'])
            domains['subdomain'][subdomain]['cname'].extend(sub_a_record['cname'])

        for txt_record in ns_records['zone_record']['txt']:
            subdomain = txt_record['service']
            domains['subdomain'][subdomain] = {'txt': []}
            domains['subdomain'][subdomain]['txt'].extend(txt_record['value'])

        domains['dns']['ns'].extend(ns_records['zone_record']['ns_record'])
        domains['dns']['soa'].extend(ns_records['zone_record']['soa_record'])

    # 查询 SOA 记录
    print '[*] Starting SOA Search...'
    soa_records = get_soa_record(target_domain)
    for soa_record in soa_records['soa']:
        domains['dns']['soa'].append(soa_record)

    # 查询 MX 记录
    print '[*] Starting MX Search...'
    mx_records = get_mx_record(target_domain)
    for mx_record in mx_records['mx']:
        domains['dns']['mx'].append(mx_record)
        domains['dns']['mx'][mx_record] = get_a_record(mx_record)

    # Dnsdb数据处理
    if file != '':
        print '[*] Get Dnsdb file...'
        rdata = data_integration(file)
        for key, value in rdata.items():
            if key in domains['subdomain']:
                domains['subdomain'][key].update(value)
            else:
                domains['subdomain'][key] = value

    # 子域名查询
    print '[*] Starting Subdomain Search...'
    subdomain_records = get_subdomain(target_domain)
    for subdomain in subdomain_records:
        sub_a_record = get_a_record(subdomain)
        subdomain_record = {'a': sub_a_record['a'], 'cname': sub_a_record['cname']}
        domains['subdomain'].update({subdomain: subdomain_record})

    return domains


if __name__ == '__main__':
    opts, args = options.parse_args()
    if len(sys.argv) < 2:
        print options.print_help()
        exit(-1)
    print sdomain(sys.argv[1], file=opts.file)

