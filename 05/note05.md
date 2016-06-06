note05.md

脚本功能
采集机器的自身信息
1 主机名 
echo $HOSTNAME
import socket
socket.gethostname()

In [11]: platform.node()
Out[11]: 'reboot-devops-02'

2 内存信息
cat /proc/meminfo
MemTotal -- MB GB

3 ip与mac地址
ifconfig
ip

import psutil
In [4]: psutil.net_if_addrs()
Out[4]: 
{'eth0': [snic(family=2, address='10.0.2.15', netmask='255.255.255.0', broadcast='10.0.2.255', ptp=None),
  snic(family=10, address='fe80::a00:27ff:fe2d:823a%eth0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None),
  snic(family=17, address='08:00:27:2d:82:3a', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)],
 'eth1': [snic(family=2, address='192.168.99.10', netmask='255.255.255.0', broadcast='192.168.99.255', ptp=None),
  snic(family=10, address='fe80::a00:27ff:fe82:92b9%eth1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None),
  snic(family=17, address='08:00:27:82:92:b9', netmask=None, broadcast='ff:ff:ff:ff:ff:ff', ptp=None)],
 'lo': [snic(family=2, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None),
  snic(family=10, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None),
  snic(family=17, address='00:00:00:00:00:00', netmask=None, broadcast=None, ptp=None)]}

4 cpu信息
cat /proc/cpuinfo
processor   : 0
model name  : Intel(R) Core(TM) i7 CPU       Q 720  @ 1.60GHz

5 磁盘分区信息
df -Ph
# fdisk -l

Disk /dev/sda: 10.6 GB, 10632560640 bytes


6 制造商信息
# dmidecode | grep "System Information" -A 6
System Information
    Manufacturer: innotek GmbH
    Product Name: VirtualBox
    Version: 1.2
    Serial Number: 0
    UUID: 4BBD5CB4-2B55-4E85-84D8-4C53EBB0075F
    Wake-up Type: Power Switch

7 出厂时间
# dmidecode | grep -i release
    Release Date: 12/01/2006
转换格式 YYYY-MM-DD

8 系统版本

# cat /etc/issue
CentOS release 6.6 (Final)
Kernel \r on an \m

import platform
In [13]: platform.linux_distribution()
Out[13]: ('CentOS', '6.6', 'Final')


# zabbix 相关概念
host 被监控对象 -- 对象
hostgroup  被监控对象的分组
template 模板 -- 对象，于host存放同一张表，平级
item 一个监控指标或监控项
application 对item进行分组
trigger 触发告警的规则

Macros 变量
集成

## zabbix 模板 -- 建议
命名 要和业务关联
使用集成




https://www.zabbix.com/documentation/2.4/manual/installation/install_from_packages


cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 

sed -i 's/de_DE/en_US/' /etc/sysconfig/i18n


mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo

yum -y install epel-release


rpm -ivh http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm

yum install zabbix-server-mysql zabbix-web-mysql mysql-server -y

yum install zabbix-agent -y


/etc/init.d/mysqld start
/usr/bin/mysql_secure_installation

mysql -uroot -p123456 -e "create database zabbix;"

cd /usr/share/doc/zabbix-server-mysql-2.4.0/create
mysql -uroot -p123456 zabbix < schema.sql
mysql -uroot -p123456 zabbix < images.sql
mysql -uroot -p123456 zabbix < data.sql


php.ini
```
php_value max_execution_time 300
php_value memory_limit 128M
php_value post_max_size 16M
php_value upload_max_filesize 2M
php_value max_input_time 300
php_value date.timezone "Asia/Shanghai"
```

/etc/init.d/zabbix-server start
并加入 /etc/rc.local

/etc/init.d/httpd start
chkconfig httpd on
chkconfig mysqld on


web 安装
http://192.168.99.14/zabbix

admin
zabbix

关闭selinux


pip install zabbix-client


In [1]: from zabbix_client import ZabbixServerProxy

In [2]: s = ZabbixServerProxy('http://192.168.99.14/zabbix')

In [3]: s.apiinfo.version()
Out[3]: u'2.4.8'

In [4]: s.user.login(user='Admin', password='zabbix')
Out[4]: u'39b95e0c0df956b4848fc762018b8d5b'

In [5]:  s.host.get(output=['hostid', 'host'])
Out[5]: 
[{u'host': u'Zabbix server', u'hostid': u'10084'},
 {u'host': u'reboot-ms-web-01', u'hostid': u'10107'}]

In [6]:  s.host.get(output=['extend'])
Out[6]: [{u'hostid': u'10084'}, {u'hostid': u'10107'}]

In [7]:  s.host.get(output='extend')
Out[7]: 
[{u'available': u'1',
  u'description': u'',
  u'disable_until': u'0',
  u'error': u'',
  u'errors_from': u'0',
  u'flags': u'0',



## zabbix-client 练习需求
1 创建一个reboot组
2 获取reboot组id
3 准备5台机器
4 批量创建主机，并加入到reboot组
5 将这些机器加上 Template OS Linux 这个模板

[
    {"ip": "172.16.31.12", "host": "yz-ms-web-01"},
    {"ip": "172.16.31.13", "host": "yz-ms-web-02"},
    {"ip": "172.16.31.14", "host": "yz-ms-web-03"},
    {"ip": "172.16.31.15", "host": "yz-ms-web-04"},
    {"ip": "172.16.31.16", "host": "yz-ms-web-05"}
]


## 作业1
## zabbix 与 CMDB

缓存表 -- zb_host

1 将zabbix中的host同步到缓存表(zb_host)
    字段信息
        hostid
        host
        ip
        port  10050 agent 161 snmp
        serverid
    host.get(output=['hostid', 'host', 'ip', 'port'])
    ? ip,port 怎么取 ?
    [
        {
            "hostid": 10021,
            "host": "yz-ms-web-01",
            "ip": "192.168.99.11",
            "port": "10051"
        },
        {
            "hostid": 10022,
            "host": "yz-ms-web-02",
            "ip": "192.168.99.12",
            "port": "10051"
        }
    ]

2 讲cmdb里的信息同步到缓存表里
    server.get(output=["server_id", "hostname", "ip"])

3 匹配后，插入缓存表
    [
        {
            "hostid": 10021,
            "host": "yz-ms-web-01",
            "ip": "192.168.99.11",
            "port": "10051",
            "server_id": 22
        },
        {
            "hostid": 10022,
            "host": "yz-ms-web-02",
            "ip": "192.168.99.12",
            "port": "10051",
            "server_id": 21
        }
    ]

4 已知的问题
第一次同步
    哪些host在zabbix里
        pass
    哪些不在zabbix
        s.host.create()

匹配不上
    ip可以匹配，hostname不匹配
    hostname匹配，ip不匹配

5 后续同步
    检查hostname, ip, port 有没有变更
    s.host.update()
    s.host.update() 成功：
        更新缓存表




## 作业2 zabbix
1 创建一个network组
2 获取network组id
3 准备5台网络设备
4 批量创建主机，并加入到network组
5 将这些机器加上 Template SNMP Device 这个模板

[
    {"ip": "10.20.31.101", "host": "juniper-device-01"},
    {"ip": "10.20.31.102", "host": "juniper-device-02"},
    {"ip": "10.20.31.103", "host": "juniper-device-03"},
    {"ip": "10.20.31.104", "host": "juniper-device-04"},
    {"ip": "10.20.31.105", "host": "juniper-device-05"}
]

备注： 走snmp 端口为 161

interface和port要修改

## 作业3
flask + uwsgi + nginx
搭建网站，运行起来

## 作业4
物理机取内存
    几根内存条，每根内存条的大小。


主机信息自动同步过去


server_modify 要求
    业务线，产品线，状态必须要能修改


## 作业5
web界面的 "同步到zabbix" 按钮
左边： 不在zabbix中的机器
右边：zabbix中的hostgroup 同步到哪个组


## 作业6 
练习2遍，左右的zabbix api

场景：
一批机器突然故障，运维已知，想要关掉报警
但是不能关数据采集