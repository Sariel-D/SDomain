#!/usr/bin/env python
# encoding: utf-8


# Data From File


import platform
import os


def coupling_file_addr(file_addr):
    current_os = platform.system().lower()
    print '[!] 当前系统版本({0}), 尝试转换不规范路径.'.format(current_os)
    if current_os == 'win':
        file_addr = file_addr.replace('/', '\\')
    elif current_os == 'linux' or os == 'unix':
        file_addr = file_addr.replace('\\', '/')
    else:
        pass
    return file_addr


def check_file_exist(file_addr):
    if os.path.exists(file_addr):
        return True
    else:
        return False


def data_integration(file_addr):
    domains = {}
    if not check_file_exist(file_addr):
        return domains
    with open(coupling_file_addr(file_addr)) as rfile:
        for line in rfile:
            line = eval(line)
            if len(line):
                domains[line['host']] = {line['type']: [line['value']]}
    return domains
