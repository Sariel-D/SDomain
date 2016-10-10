#!/usr/bin/env python
# encoding: utf-8


from config import default_dns_setting as dns_set
import dns.resolver
import dns.zone


_res = dns.resolver.Resolver()
_res.nameservers = dns_set['nameservers']
_res.timeout = dns_set['timeout']


######################################################################
#
#                               A
#
######################################################################
#
# 查询所有A记录
#
def get_a_record(domain):
    domains = {'a': [], 'cname': []}
    try:
        a = _res.query(domain, 'A')
        for j in a.response.answer:
            if j.rdtype == 1:  # A
                # 1. 匹配ip
                # from network.ipv4 import matching_ip
                # a_list = matching_ip(j.to_text())
                # domains['a'] = a_list
                #
                # 2. 转化list, 分割提取
                for single_a_record in list(j):
                    a_list = single_a_record.to_text().split()
                    domains['a'].append(a_list[-1])
            elif j.rdtype == 5:  # CNAME
                for single_cname_record in list(j):
                    cname_list = single_cname_record.to_text().split()
                    domains['cname'].append(cname_list[-1])
            else:
                pass
    except:
        pass
    return domains


######################################################################
#
#                             CNAME
#
######################################################################
# !!!
# 查询所有CNAME记录, 这个外网探测时候基本没有作用，有实例后修改代码
#
def get_cname_record(domain):
    domains = {'cname': []}
    try:
        cname = _res.query(domain, 'CNAME')
        for j in cname.response.answer:
            for single_cname_record in list(j):
                cname_list = single_cname_record.to_text().split()
                domains['cname'].append(cname_list[-1])
    except:
        pass
    return domains


######################################################################
#
#                               MX
#
######################################################################
#
# 查询所有MX记录
#
def get_mx_record(domain):
    domains = {'mx': []}
    try:
        mx = _res.query(domain, 'MX')
        for j in mx.response.answer:
            for single_mx_record in list(j):
                mx_list = single_mx_record.to_text().split()
                domains['mx'].append(mx_list[-1])
    except:
        pass
    return domains


######################################################################
#
#                               NS
#
######################################################################
#
# 查询所有NS记录
#
def get_ns_record(domain):
    domains = {'ns': [], 'zone_vul': False, 'zone_record':None}
    try:
        ns = _res.query(domain, 'NS')
        ns_records = []
        for i in ns.response.answer:
            for j in i.items:
                single_ns_record = j.to_text().rstrip('.')
                # !!!
                # 这里需要检查白名单
                #
                status = check_zone_transfer_vul(single_ns_record, domain)
                if not status:
                    # 没有域传送漏洞
                    continue
                else:
                    if domains['zone_vul']:
                        # 已经处理过域传送漏洞
                        pass
                    else:
                        domains['zone_vul'] = True
                        domains['zone_record'] = get_ns_record_from_zone_vul(single_ns_record, domain)
                ns_records.append(single_ns_record)
        domains['ns'] = ns_records
    except:
        pass
    return domains


#
# 检查是否有域传送漏洞
#
def check_zone_transfer_vul(ns_record, domain):
    try:
        # @type vul : generator
        vul = dns.query.xfr(ns_record, domain)
        return True
    except:
        return False


#
# 从域传送漏送中提取信息
#
def get_ns_record_from_zone_vul(ns, domain):
    domains = {}
    a_record = []
    soa_record = []
    cname_record = []
    ns_record = []
    txt_record = []
    dns_xfr = dns.query.xfr(ns, domain)
    # @type zone_res : class dns.message.Message
    for message in dns_xfr:
        # @type origin : class dns.name.Name
        origin = message.origin.to_text()
        # @type single_message : class dns.rrset.RRset(ns.rdataset.Rdadaset)
        for single_message in message.answer:
            # The definition of value of rdtype in dns.rdatatype
            if single_message.rdtype == 1:  # A
                record_dict = {}
                record_list = single_message.to_text().split()
                record_name = "%s.%s" % (record_list[0], origin)
                record_value = record_list[-1]
                record_dict['service'] = record_name.rstrip('.')
                record_dict['value'] = record_value
                record_dict['origin'] = origin
                a_record.append(record_dict)
                # print "A: %s >> %s <--> %s" % (
                #     record_dict['origin'], record_dict['service'], record_dict['value'])
            elif single_message.rdtype == 2:  # NS
                record_dict = {}
                record_list = single_message.to_text().split()
                record_name = "%s.%s" % (record_list[0], origin)
                record_value = record_list[-1].rstrip('.')
                record_dict['service'] = record_name.rstrip('.')
                record_dict['value'] = record_value
                #  !!!
                #  value需要判断是否非完整记录，可能需要加origin
                #
                record_dict['origin'] = origin
                if record_dict not in ns_record:
                    ns_record.append(record_dict)
                    # print "NS: %s >> %s <--> %s" % (
                    #     record_dict['origin'], record_dict['service'], record_dict['value'])
            elif single_message.rdtype == 5:  # CNAME
                record_dict = {}
                record_list = single_message.to_text().split()
                record_name = "%s.%s" % (record_list[0], origin)
                record_value = record_list[-1]
                record_dict['service'] = record_name.rstrip('.')
                record_dict['value'] = record_value
                #  !!!
                #  value需要判断是否www/mail/或者直接A记录，前面的需要加origin完整化
                #
                record_dict['origin'] = origin
                cname_record.append(record_dict)
                # print "CNAME: %s >> %s <--> %s" % (
                #     record_dict['origin'], record_dict['service'], record_dict['value'])
            elif single_message.rdtype == 6:  # SOA
                base_index = 4
                record_dict = {}
                record_value = []
                record_list = single_message.to_text().split()
                record_name = "%s.%s" % (record_list[0], origin)
                while -1 != record_list[base_index].find('.'):
                    record_value.append(record_list[base_index].rstrip('.'))
                    base_index += 1
                record_dict['service'] = record_name.rstrip('.')
                record_dict['value'] = record_value
                record_dict['origin'] = origin
                if record_dict not in soa_record:
                    soa_record.append(record_dict)
                    # print "SOA: %s >> %s <--> %s" % (
                    #     record_dict['origin'], record_dict['service'], record_dict['value'])
            elif single_message.rdtype == 16:  # TXT
                record_dict = {}
                record_list = single_message.to_text().split()
                record_name = "%s.%s" % (record_list[0], origin)
                record_value = record_list[-1]
                record_dict['service'] = record_name.rstrip('.')
                record_dict['value'] = record_value
                record_dict['origin'] = origin
                txt_record.append(record_dict)
                # print "TXT: %s >> %s <--> %s" % (
                #     record_dict['origin'], record_dict['service'], record_dict['value'])
            elif single_message.rdtype == 99:  # SPF
                print '[!] dns_func.get_ns_record_from_zone_vul SPF部分代码需要修改.'
                print '[-]', ns
            elif single_message.rdtype == 255:  # ANY
                print '[!] dns_func.get_ns_record_from_zone_vul ANY部分代码需要修改.'
                print '[-]', ns
            else:
                pass
    domains['a'] = a_record
    domains['cname'] = cname_record
    domains['ns'] = ns_record
    domains['soa'] = soa_record
    domains['txt'] = txt_record
    return domains


######################################################################
#
#                               SOA
#
######################################################################
#
# 查询所有SOA记录
#
def get_soa_record(domain):
    domains = {'soa': []}
    base_index = 0
    try:
        soa = _res.query(domain, 'SOA')
        for j in soa.response.answer:
            for single_soa_record in list(j):
                record_list = single_soa_record.to_text().split()
                while -1 != record_list[base_index].find('.'):
                    domains['soa'].append(record_list[base_index].rstrip('.'))
                    base_index += 1
    except:
        pass
    return domains


######################################################################
#
#                               TXT
#
######################################################################
#
# 查询所有TXT记录
#
def get_txt_record(domain):
    domains = {'txt': []}
    try:
        txt = _res.query(domain, 'txt')
        for j in txt.response.answer:
            for single_txt_record in list(j):
                domains['txt'].append(single_txt_record.to_text())
    except:
        pass
    return domains


if __name__ == '__main__':
    print get_ns_record('zonetransfer.me')
    print get_a_record('sina.com')
    print get_mx_record('sina.com')
    print get_soa_record('sina.com')
    print get_txt_record('baidu.com')
    print get_cname_record('staging.zonetransfer.me')
