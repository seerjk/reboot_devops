note04.md

# 03作业
删除某条记录
不要从数据库直接删除，数据宝贵

给每张表增加一个字段 修改status字段1-->0来实现删除
    status
        0   已删除
        1   正常（默认）

modules.py 增加
# status 是否删除  normal 1
    status           = db.Column(db.Integer, index=True, nullable=False)

更新db
python manage.py db migrate
python manage.py db upgrade

需求：
1 点击删除按钮
2 触发 ajax事件
3 服务端告知，删除成功
4 从页面删除这条记录
    刷新 reload()
    通过JS，将这条数据从页面删除  不用刷新



ip_info
{
    ip:xxx,
    mac:xxx
},
{
    ip:xxx,
    mac:xxx
},
{
    ip:xxx,
    mac:xxx
}

{ip:xxx, mac:xxx},{ip:xxx, mac:xxx},{ ip:xxx, mac:xxx}

服务器
    web
        添加服务器
        修改服务器
    采购流程 自动入库
    数据自动上报
        cpu, mem, disk ... 等


db中alembic_version表，与项目中migrations目录对应，
如果删除alembic_version表，需要将migrations目录也删除

## 作业1
utils.__init__.py
继续优化，抽出一样的代码做函数

## 作业2
idc和manufacturers 变为类，
基类 -- Idc 和 Manufactureers 不同

## 作业3 完成
server_doadd
server_modify

## zabbix
按照官方教程
2.4 yum rpm 安装
一个服务器
2个client