# note 01

1 计算机语言语法
    python
    javascript

2 数据结构与算法
    清华大学 严蔚敏 计算机数据结构
        最多看到第6章
        用python实现一遍

3 工程实现思路
    devops 课程中
        saltstack 二次开发
        zabbix 二次开发
    api的设计
        为啥要api
        为啥一个个定义参数
        命名
        安全
        为啥不要界面

4 实践


* 怎么把需求、功能做成系统，反复的去用。
* 去学习PHP

参数设置、安全问题、性能调优、解耦、数据库设计、异常判断  这些都是工程思想

> 面微信支付的时候，问了个问题，
什么时候用水平触发，什么时候用边缘触发，也就是场景的问题？
结合对方的场景来解答问题
比如：已知峰值情况、突发峰值情况、日常情况
结合微信支付的场景，抢红包。吃饭时，午饭晚饭，节假日
低流量时，什么情况。

> 觉得微博上，更新一条微博，是通过推，还是拉的方式，通知该账号的粉丝
结合场景，说明什么是推和拉，知道怎么用。


课程要求：
    出席考勤
    作业
    复习
        回顾以前的课程。

# 开发环境
gliffy 流程图

linux server (CentOS6/7)
Git 版本控制
virtual box 或者 vmware 加入系统环境变量 PATH
    支持cmd命令行控制虚拟机
PC vagrant  (vagrant file) linux windows macos
    做为开发环境，pc代码映射到linux虚拟机的目录
    python 环境
pycharm IDE 方便查看源代码和文档

# vagrant 使用
https://github.com/tommy-muehle/puppet-vagrant-boxes/releases/download/1.0.0/centos-6.6-x86_64.box

vagrant box add “centos 6.6” centos-6.6-x86_64.box
vagrant box list
vagrant init "centos 6.6"
启动当前目录下的vm
vagrant up

vagrant ssh

vagrant --help

关机
vagrant halt

vagrantfile 判断是否是工作目录

vagrant global-status


vagrantfile需要配置
```
config.vm.network "forwarded_port", guest: 8000, host: 8000
```

vagrant reload


# python 环境
yum install -y gcc gcc-c++ zlib-devel openssl-devel readline-devel lrzsz
echo $LANG
LANG=en_US.UTF-8
python 2.11

tar -xzf Python-2.7.11.tgz 
cd Python-2.7.11
./configure --help
./configure 
./configure --prefix=/usr/local/python27
make && make install

tar -xzf setuptools-20.10.1.tar.gz 
cd setuptools-20.10.1
/usr/local/python27/bin/python setup.py install

/usr/local/python27/bin/easy_install pip

/usr/local/python27/bin/pip install virtualenv
mkdir /data
/usr/local/python27/bin/virtualenv /data/python27env
source /data/python27env/bin/activate
pip list
pip install ipython
ipython


pyenv 工具

# 运维自动化概述

CMDB
API
可视化
    前端

安全
    分享
权限
    rbac权限

资源平台
监控平台
性能分析
发布平台：
    代码上线，运维平台代码 rsync
    线上业务代码上线

flask hello world
看书 前5章

## CMDB的演进
第一阶段 -- 早期
    人工大脑、Excel、wiki
    主机名、IP地址、机房、机柜、操作系统版本。。。
第二阶段 -- 
    CMDB、资源平台
    人、物、业务、权限
    硬件相关：供应商、制造商、出厂日期、服务器类型、st/sn号、自动以资产号、IDC、机柜、机柜内位置、到保日期、有无UPS电源、上架日期、RAID、RAID卡型号、远程管理卡类型、远程管理IP、电影功率、是否是虚拟机、宿主机
    系统相关：操作系统类型、操作系统版本、主机名、内网IP、MAC地址、CPU型号、硬盘信息、内存、服务器状态（线上，线下，测试，故障）、备注
    业务相关：业务线、产品线、故障处理人、运维接口人、开发接口人
    服务的注册，未注册的，有agent kill掉。


## API

图 api_intro

先登录，成功后，返回token
后面的请求携带token (登录与权限)
DB记录 token + 一系列权限

API需求分析：
    http://admin.51reboot.com/page/apidoc
    浏览器 -- nginx 基于http 再次封装
    php去调用API，用curl模块


基于http实现，如果请求量特别大怎么办？
对web做HA高可用，API负载均衡
AWS的实现，完全的API

### API实现
流程图 ppt
前端：用户请求API，返回结果
后端：验证json，验证权限，执行模块，返回结果

### 伪代码实现API

* 作业：伪代码转换为python代码



我们给cmdb定义了一套接口，供外围调用。
1.外围系统A发送request：增加一个主机
2.cmdb接收到关于增加主机的API请求，做以下判断
验证 json数据，根据json各个属性的验证，返回对应的验证结果
验证通过后，判断有没有一个管理主机的 模块
存在一个管理主机的模块，就调用 该模块的方法，返回调用结果。


把伪代码转化为代码，最终是可以直接执行成功的。
大家可以拆分两部分写作业    
1:  通过 API框架＋模块 跑通  
2: flask＋API＋模块

auth可以先不写，仅判断有没有这个字段

