#!/usr/bin/python
# coding:utf-8

from flask import current_app
from app.base import AutoLoad

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