#!/usr/bin/env python
# encoding: utf-8


from spider import slsubdomain, spbaidu, spgoogle, spbing, spaizhan


def get_subdomain(domain):
    domains = []

    #
    # slsubdomain
    domains.extend(slsubdomain.get_alexa_records(domain))
    domains.extend(slsubdomain.get_links_records(domain))
    domains.extend(slsubdomain.get_netcraft_records(domain))
    domains.extend(slsubdomain.get_sitedossier_records(domain))

    #
    # bing\baidu\google\aizhan
    domains.extend(spbing.bing_scan('domain', domain).keys())
    domains.extend(spbaidu.baidu_scan('domain', domain).keys())
    domains.extend(spgoogle.google_scan('site', domain).keys())
    domains.extend(spaizhan.aizhan_scan(domain).keys())

    return domains


if __name__ == '__main__':
    print get_subdomain('baidu.com')