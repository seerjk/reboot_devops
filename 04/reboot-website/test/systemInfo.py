#!/usr/bin/python
# coding:utf-8

import socket
import commands
import psutil

def get_hostname():
    hostname = socket.gethostname()
    return hostname


def get_mem_info():
    quite_code, output = commands.getstatusoutput("cat /proc/meminfo")
    # mem_total = 0.0
    for line in output.split('\n'):
        # print line
        items = line.strip().split()
        # print items
        if items[0] == "MemTotal:":
            # print type(items[1])
            # print items[1]
            mem_total = int(items[1]) / 1024.0
            break

    return mem_total


def get_ip_mac():
    net_info = psutil.net_if_addrs()
    print type(net_info['eth0'])
    for i in net_info['eth0']:
        # items = i.strip(')').strip('snic(').split(',')
        # print items
        pass


if __name__ == "__main__":
    # print get_hostname()
    # print get_mem_info()
    get_ip_mac()