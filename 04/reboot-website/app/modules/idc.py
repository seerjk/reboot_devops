#!/usr/bin/python
# coding:utf-8

from app.models import Idc
from flask import current_app
from app.models import db
from app.utils import check_field_exists
from app.utils import check_output_field
from app.utils import check_order_by
from app.utils import check_limit
from app.utils import process_result
from app.utils import check_update_params

def create(**kwargs):
    # 1 获取参数
    # print kwargs

    # 2 检查参数
    # for field in kwargs.keys():
    #     # 2.1 验证参数是否在idc表中
    #     if not hasattr(Idc, field):
    #         # logging
    #         current_app.logger.warning(
    #             "参数错误，{} 不在Idc这张表中".format(field)
    #         )
    #         raise Exception("params error: {}".format(field))
    #     # 2.2 不能为空
    #     if not kwargs.get(field, None):
    #         # logging
    #         current_app.logger.warning(
    #             "参数错误，{} 不能为空".format(field)
    #         )
    #         raise Exception("{} 不能为空".format(field))
    check_field_exists(Idc, kwargs)

    # 3 插入到数据库
    idc = Idc(**kwargs)
    db.session.add(idc)
    try:
        db.session.commit()
    except Exception, e:
        # logging
        current_app.logger.warning(
            "commit error: {}".format(e.message)
        )
        raise Exception("commit error")

    # 4 返回插入的状态
    return idc.id


def get(**kwargs):
    # output: [idc_name, user_interface, user_phone]
    # where: {
    #     id: 1
    # }
    # limit: 10
    # order_by: id
    # 1 整理条件
    output = kwargs.get("output", [])
    limit = kwargs.get("limit", 10)
    order_by = kwargs.get("order_by", "id desc")
    where = kwargs.get("where", {})

    # 2 验证
    # 验证output
    # if not isinstance(output, list):
    #     # logging
    #     current_app.logger.warning("output 类型必须为list")
    #     raise Exception("output 类型必须为list")
    #
    # for field in output:
    #     if not hasattr(Idc, field):
    #         # logging
    #         current_app.logger.warning("{}这个output输出的字段不存在idc表中".format(field))
    #         raise Exception("{}这个output输出的字段不存在idc表中".format(field))
    check_output_field(Idc, output)

    # 验证 order_by，字符串分割，字段是否在表中   第二个字段必须为asc desc
    # tmp_order_by = order_by.split()
    # if len(tmp_order_by) != 2:
    #     # logging
    #     current_app.logger.warning("order_by 参数个数不正确")
    #     raise Exception("order_by 参数不正确")
    #
    # order_by_list = ['desc', 'asc']
    # if tmp_order_by[1].lower() not in order_by_list:
    #     # logging
    #     current_app.logger.warning("order_by 第二个参数不正确，值必须为desc或者asc")
    #     raise Exception("order_by 第二个参数不正确，值必须为desc或者asc")
    #
    # if not hasattr(Idc, tmp_order_by[0]):
    #     # logging
    #     current_app.logger.warning("排序字段 {} 不在idc表中".format(tmp_order_by[0]))
    #     raise Exception("排序字段 {} 不在idc表中".format(tmp_order_by[0]))
    order_by_list = check_order_by(Idc, order_by)

    # 验证 limit 必须为数字
    # if not str(limit).isdigit():
    #     # logging
    #     current_app.logger.warning("limit的值必须为数字")
    #     raise Exception("limit的值必须为数字")
    check_limit(limit)

    # 验证 where 条件，先不验证
    pass

    # print callable(getattr(getattr(Idc, "id"), "desc"))
    # 函数对象
    # getattr(getattr(Idc, tmp_order_by[0]), tmp_order_by[1])
    # 调用函数
    # getattr(getattr(Idc, tmp_order_by[0]), tmp_order_by[1])()

    data = db.session.query(Idc).filter_by(**where)\
        .order_by(getattr(getattr(Idc, order_by_list[0]), order_by_list[1])())\
        .limit(limit).all()
    db.session.close()

    # process result
    # ret = []
    # # print data
    # for obj in data:
    #     # print dir(obj)
    #     # print obj.__dict__
    #     if output:
    #         tmp = {}
    #         for f in output:
    #             tmp[f] = getattr(obj, f)
    #         ret.append(tmp)
    #     else:
    #         tmp = obj.__dict__
    #         tmp.pop("_sa_instance_state")
    #         ret.append(tmp)
    return process_result(data, output)

    # return ret


def update(**kwargs):
    data = kwargs.get("data", {})
    where = kwargs.get("where", {})

    # # 1 验证data
    # if not data:
    #     raise Exception("data为空，没有需要更新的")
    #
    # for field in data.keys():
    #     if not hasattr(Idc, field):
    #         raise Exception("需要更新的 {} 字段在idc表不存在".format(field))
    #
    # # 2 验证where
    # if not where:
    #     raise Exception("需要提供where条件")
    #
    # # 3 更新必须提供id，只按照id更新
    # if not where.get("id", None):
    #     raise Exception("需要提供id作为更新条件")
    #
    # # id 要为数字且大于0的整数
    # if str(where.get("id")).isdigit():
    #     if int(where.get("id")) <= 0:
    #         raise Exception("id的值为大于0的整数")
    # else:
    #     raise Exception("条件中的id必须为数字")
    check_update_params(Idc, data, where)

    # update
    # ret = db.session.query(Idc).filter_by(**where).update(**data)
    # 调用模块执行出现错误：update() got an unexpected keyword argument 'rel_cabinet_num'
    ret = db.session.query(Idc).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception, e:
        # logging
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")

    # print ret
    return ret


def delete(**kwargs):
    """
    根据ID来删除，需要传入where条件的id
    :param kwargs:
    :return:
    """
    where = kwargs.get("where", {})

    # 1 验证where
    if not where:
        raise Exception("删除，必须提供where条件")

    # 2 where中必须只有id
    # 2.1 where的keys只有一个
    if len(where.keys()) != 1:
        raise Exception("删除的where条件只能有1个字段")

    # 2.2 删除必须提供id
    if not where.get("id", None):
        raise Exception("删除，需要提供id作为条件")

    # 3 id必须为数字，且大于0
    if not str(where.get("id")).isdigit():
        raise Exception("删除，id必须为数字")

    # 4 执行删除，处理异常
    ret = db.session.query(Idc).filter_by(**where).delete()

    try:
        db.session.commit()
    except Exception, e:
        current_app.logger.warning("commit error: {}".format(e.message))
        raise Exception("commit error")

    return ret
