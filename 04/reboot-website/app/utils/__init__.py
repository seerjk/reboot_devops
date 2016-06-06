#!/usr/bin/python
# coding:utf-8

from flask import current_app
from app.base import AutoLoad
from flask import render_template


def api_action(method="", params={}):
    # api 和 web nginx在同一个主机，或者域名下
    try:
        module, func = method.split(".")
    except ValueError, e:
        # logging
        current_app.logger.warning("method传值错误：{}".format(e.message))
        # 框架之外，没有异常处理
        return False

    at = AutoLoad()
    if not at.isValidModule(module):
        # logging
        current_app.logger.warning("{} 模块不可用".format(module))
        return False

    if not at.isValidMethod(func):
        current_app.logger.warning("{} 函数不可用".format(func))
        return False

    # 处理调用module.method过程的异常，method会raise Exception
    try:
        called = at.getCallMethod()
        if callable(called):
            return called(**params)
        else:
            # logging
            current_app.logger.warning("{}.{} 函数不能被调用".format(module, func))
            return False
    except Exception, e:
        current_app.logger.warning("Web 调用模块 {}.{} 执行中出错：{}".format(module, method, e.message))
        return False


def api_action_diff_host(method="", params=""):
    # api 和 web nginx 不在同一个主机，类似测试test_api的调用方法
    url = "http://ip:8000/api"
    header = {
        "content-type": "application/json"
        # "content-type": "application/jsonaa"
    }
    data = {
        "jsonrpc": 2.0,
        "method": "idc.get",
        "id": 0,
        "auth": None,
        "params": {
            "output": ["id", "name", "email", "rel_cabinet_num"],
            "order_by": "id desc",
            "limit": 15
        }
    }
    # "params": {
    #     "name": "rock abcdedf"
    # }
    # "params": 1

    # r = requests.get(url, headers=header, params=json.dumps(data))
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content


def check_field_exists(obj, data, field_none=[]):
    for field in data.keys():
        # 2.1 验证参数是否在idc表中
        if not hasattr(obj, field):
            # logging
            current_app.logger.warning(
                "参数错误，{} 不在这张表中".format(field)
            )
            raise Exception("params error: {}".format(field))
        # 2.2 field为空处理
        if not data.get(field, None):
            # field 可以为空
            if field_none == False:
                continue

            # 不能为空的field 抛出异常
            if field not in field_none:
                # logging
                current_app.logger.warning(
                    "参数错误，{} 不能为空".format(field)
                )
                raise Exception("{} 不能为空".format(field))


def check_output_field(obj, output):
    if not isinstance(output, list):
        # logging
        current_app.logger.warning("output 类型必须为list")
        raise Exception("output 类型必须为list")

    for field in output:
        if not hasattr(obj, field):
            # logging
            current_app.logger.warning("{}这个output输出的字段不存在idc表中".format(field))
            raise Exception("{}这个output输出的字段不存在idc表中".format(field))


def check_order_by(obj, order_by):
    tmp_order_by = order_by.split()
    if len(tmp_order_by) != 2:
        # logging
        current_app.logger.warning("order_by 参数个数不正确")
        raise Exception("order_by 参数不正确")

    order_by_list = ['desc', 'asc']
    if tmp_order_by[1].lower() not in order_by_list:
        # logging
        current_app.logger.warning("order_by 第二个参数不正确，值必须为desc或者asc")
        raise Exception("order_by 第二个参数不正确，值必须为desc或者asc")

    if not hasattr(obj, tmp_order_by[0]):
        # logging
        current_app.logger.warning("排序字段 {} 不在idc表中".format(tmp_order_by[0]))
        raise Exception("排序字段 {} 不在idc表中".format(tmp_order_by[0]))

    return tmp_order_by


def check_limit(limit):
    if not str(limit).isdigit():
        # logging
        current_app.logger.warning("limit的值必须为数字")
        raise Exception("limit的值必须为数字")


def process_result(data, output):
    # process result
    ret = []
    # print data
    for obj in data:
        # print dir(obj)
        # print obj.__dict__
        if output:
            tmp = {}
            for f in output:
                tmp[f] = getattr(obj, f)
            ret.append(tmp)
        else:
            tmp = obj.__dict__
            tmp.pop("_sa_instance_state")
            ret.append(tmp)

    return ret


def check_update_params(obj, data, where):
    # 1 验证data
    if not data:
        raise Exception("data为空，没有需要更新的")

    for field in data.keys():
        if not hasattr(obj, field):
            raise Exception("需要更新的 {} 字段在idc表不存在".format(field))

    # 2 验证where
    if not where:
        raise Exception("需要提供where条件")

    # 3 更新必须提供id，只按照id更新
    if not where.get("id", None):
        raise Exception("需要提供id作为更新条件")

    # id 要为数字且大于0的整数
    if str(where.get("id")).isdigit():
        if int(where.get("id")) <= 0:
            raise Exception("id的值为大于0的整数")
    else:
        raise Exception("条件中的id必须为数字")


def jump(ret, success_url="/", error_url="/"):
    success = "public/success.html"
    error = "public/error.html"

    if ret:
        return render_template(success, next_url=success_url)
    else:
        return render_template(error, next_url=error_url)


def list_to_dict(obj_list, key, value):
    ret = {}
    for obj in obj_list:
        try:
            ret[obj[key]] = obj[value]
        except:
            pass
    return ret

