note03.md

logging

info 正常执行信息
debug 调试信息，线上环境关闭debug
warning
error

# sqlalchemy

# 安装配置mysql
yum install install mysql mysql-server mysql-devel
/etc/init.d/mysqld start
/usr/bin/mysql_secure_installation
mysql -uroot -p123456

create database reboot CHARACTER SET utf8;

pip install MySQL-python

sqlalchemy 建表
# python manage.py db --help
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

mysql> show tables;
+------------------+
| Tables_in_reboot |
+------------------+
| alembic_version  |  版本信息表，用于回滚
| idc              |  idc表
+------------------+


# idc.py
def create(params):
    # 创建一条IDC记录
    pass

def get():
    # 获取IDC信息
    pass

def update():
    pass

def delete():
    pass

参数的定义
params
data = {
    "jsonrpc": 2.0,
    "method": "reboot.error",
    "id": 0,
    "auth": None,
    "params": {
        
    }
}

"params": {
}

create:
{
    name
    idc_name
    address
    phone
    email
    user_interface
    user_phone
    rel_cabinet_num
    pact_cabinet_num
}

get:
只输出指定的字段
    output: [idc_name, user_interface, user_phone]
    where: {
        id: 1
    }
    limit: 10
    order_by: id 


有__init__.py 的是包

vim中制表符替换为4个空格
:%s/\t/    /g

作业：
1. 删除功能
后端 delete
前端 用ajax实现

2. 删除后要把页面上的记录刷新
或者动态刷新页面

3. 其他表和页面的增删改查