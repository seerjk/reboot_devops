#!/usr/bin/python
# coding: utf-8

import socket
import psutil
import subprocess

device_white = ["eth1", "eth2", "eth3", "bond0", "bond1"]

"""
str:
    hostname
dict
    {
        eth0
        eth1
    }
[
    {"ip": 192.168.99.11,
    "mac": 00.11.22.33.44.ff}
]

disk
[100, 100]

100 G + 100 G
"""

def get_hostname():
    return socket.gethostname()


def get_meminfo():
    mem = None
    with open("/proc/meminfo") as f:
        for line in f:
            if "MemTotal" in line:
                mem = int(line.split()[1])
                break

    return mem / 1024

def get_device_info():
    ret = []
    for device, device_info in psutil.net_if_addrs().iteritems():
        if device in device_white:
            tmp_device = {}
            for snic in device_info:
                if snic.family == 2:
                    # ip
                    tmp_device['ip'] = snic.address
                elif snic.family == 17:
                    # mac
                    tmp_device['mac'] = snic.address
            ret.append(tmp_device)
    return ret

def get_cpuinfo():
    ret = {"cpu": '', "num": 0}
    with open("/proc/cpuinfo") as f:
        for line in f:
            tmp = line.strip().split(':')
            key = tmp[0].rstrip()
            if key == "model name":
                ret['cpu'] = tmp[1].lstrip()
            elif key == "processor":
                ret['num'] += 1
    return ret


def get_diskinfo():
    devs_white = ['sda', 'sdb', 'sdc']
    cmd = """/sbin/fdisk -l | grep Disk | egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # print disk_data
    ret = []

    for dev in disk_data.stdout.readlines():
        for dev_white in devs_white:
            if dev_white in dev:
                ret.append(int(dev.strip().split(",")[1].split()[0]) / 1024 / 1024 / 1024)

    return ret

def get_manufacturer():
    pass

def get_rel_date():
    pass

def get_os_version():
    pass


if __name__ == "__main__":
    # print get_device_info()
    # print get_cpuinfo()
    print get_diskinfo()