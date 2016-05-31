#!/usr/bin/python
# coding:utf-8

import os
import imp
# import string
import sys
import json
from flask import current_app

class AutoLoad():
    """
    自动加载模块类
    """
    def __init__(self):
        # 指定项目自动加载模块的目录
        current_dir = os.path.dirname(__file__)
        # print "c:", current_dir

        self.modules_dir = os.path.abspath(os.path.join(current_dir, "..", "modules"))
        # print self.modules_dir

        # logging
        current_app.logger.debug(
            "自动加载模块的目录为：{}".format(self.modules_dir)
        )

        # idc.get
        self.module_name = ""           # 模块名字
        self.func = ""                  # 函数名称
        self.module = None              # 已加载的模块


    def isValidModule(self, module_name):
        """
        验证模块是否可用
        :param module_name: 需要导入的模块名
        :return: True/False
        """
        # logging
        current_app.logger.debug(
            "验证模块是否可用，模块名为：{}".format(module_name)
        )

        self.module_name = module_name
        return self._load_module()


    def isValidMethod(self, func):
        """
        验证函数是否可用
        :param func: 函数名
        :return: True/False
        """
        self.func = func
        # logging
        current_app.logger.debug(
            "验证模块 {} 是否存在 {} 属性".format(self.module_name, self.func)
        )

        if self.module is None:
            # logging -- self.module 是已经加载的模块
            current_app.logger.warning(
                "函数验证失败，没有验证模块"
            )
            return False
        # print "hasattr: ", hasattr(self.module, self.func)
        return hasattr(self.module, self.func)

    def getCallMethod(self):
        """
        返回执行的函数
        :return: func
        """
        # logging
        current_app.logger.debug(
            "获取可执行的函数"
        )

        if hasattr(self.module, self.func):
            # print "aaa"
            # print "getattr: ", getattr(self.module, self.func, None)
            return getattr(self.module, self.func, None)
        return None

    def _load_module(self):
        """
        动态加载模块
        :return:
        """
        # logging
        current_app.logger.debug(
            "尝试加载 {} 模块".format(self.module_name)
        )

        ret = False
        # 列出模块目录下所有的文件, ls modules
        for file_name in os.listdir(self.modules_dir):
            # 遍历模块目录下的所有文件
            if file_name.endswith(".py"):
                # 如果文件名是以.py结尾
                module_name = file_name.rstrip(".py")       # 从文件名中取出模块名
                if module_name != self.module_name:
                    # 当前遍历的这个py文件，不是我们想要导入的那个py文件
                    continue
                fp, pathname, desc = imp.find_module(module_name, [self.modules_dir])
                # print "fp: {}".format(fp)
                # print "pathname: {}".format(pathname)
                # print "desc: {}".format(desc)

                if not fp:
                    continue
                try:
                    self.module = imp.load_module(module_name, fp, pathname, desc)
                    ret = True
                    # logging
                    current_app.logger.debug(
                        "加载 {} 模块成功".format(self.module_name)
                    )
                except Exception, e:
                    pass
                    # logging
                    current_app.logger.debug(
                        "加载 {} 模块失败".format(self.module_name)
                    )
                    # 失败返回False
                finally:
                    fp.close()

                break
        return ret


class Response():
    def __init__(self):
        self.data = None            # 返回的数据
        self.errorCode = 0          # 执行过程中的错误代码
        self.errorMessage = None


class JsonRpc():
    def __init__(self):
        self.jsonData = None
        self.VERSION = "2.0"
        self._response = {}         # 返回的结果

    def execute(self):
        if self.jsonData.get("id", None) is None:
            self.jsonError(-1, 102, "id 没有传")
            # logging
            current_app.logger.error(
                "请求的参数中没有id，或者id为None"
            )

            return self._response

        if self.validate():
            # 数据验证通过
            # logging
            current_app.logger.debug("验证json格式成功")

            params = self.jsonData['params']
            print "params: ", params
            auth = self.jsonData['auth']
            module, func = self.jsonData['method'].split(".")
            ret = self.callMethod(module, func, params, auth)
            print "ret: ", ret.data
            self.processResult(ret)

        return self._response

    def validate(self):
        """
        验证json数据格式
        :return:
        """
        if self.jsonData is None:
            self.jsonError(-1, 101, u"没有指定json数据")
            # logging
            current_app.logger.warning("没有传json数据")

            return False

        # 验证是否有指定的属性：一共有5个，jsonrpc, methdod, id, auth, params

        # if self.jsonData.get("jsonrpc", None) is None:
        #     self.jsonError(-1, 102, "jsonrpc 没有传")
        #     return False
        #
        # if self.jsonData.get("method", None) is None:
        #     self.jsonError(-1, 103, "method 没有传")
        #     return False
        #
        # if self.jsonData.get("id", None) is None:
        #     self.jsonError(-1, 104, "id 没有传")
        #     return False
        #
        # if not self.jsonData.has_key('auth'):
        #     self.jsonError(-1, 105, "auth 没有传")
        #     return False
        #
        # if self.jsonData.get("params", None) is None:
        #     self.jsonError(-1, 106, "params 没有传")
        #     return False

        attributes = ["jsonrpc", "method", "id", "auth", "params"]
        for attr in attributes:
            # if attr not in self.jsonData.keys():
            if not self.jsonData.has_key(attr):
                self.jsonError(self.jsonData['id'], 102, "{} 没有传".format(attr))
                # logging
                current_app.logger.warning("请求的参数中，{} 没有传".format(attr))
                return False

        # jsonrpc的值  2.0
        if str(self.jsonData["jsonrpc"]) != "2.0":
            self.jsonError(self.jsonData['id'], 103, u"jsonrpc版本要为2.0")
            # logging
            current_app.logger.warning("jsonrpc版本正确，应该为 {}".format(self.VERSION))
            return False

        # method 必须有"."，且使用点分割的只有两个元素，不能为空
        actions = self.jsonData["method"].split('.')
        if len(actions) != 2:
            self.jsonError(self.jsonData['id'], 108, "method 错误，应该为点分割的两个字符串")
            # logging
            current_app.logger.warning(
                "method: '{}' 错误，应该为点分割的两个字符串".format(self.jsonData["method"])
            )
            return False

        if not actions[0] or not actions[1]:
            self.jsonError(self.jsonData['id'], 108, "method 错误，应该为点分割的两个字符串，且不能为空")
            # logging
            current_app.logger.warning(
                "method: '{}' 错误，应该为点分割的两个字符串，且不能为空".format(self.jsonData["method"])
            )
            return False

        # id 要是数字
        if not str(self.jsonData["id"]).isdigit():
            self.jsonError(self.jsonData['id'], 109, "id 必须为数字")
            # logging
            current_app.logger.warning(
                "id为 {}，类型错误，id必须为数字类型".format(self.jsonData["id"])
            )
            return False

        # auth 必须要有，可以为None

        # params 必须为dict类型，dict可以为None
        if not isinstance(self.jsonData["params"], dict):
            # logging
            current_app.logger.warning(
                "params为 '{}' 类型错误，必须为字典类型".format(self.jsonData["params"])
            )
            self.jsonError(self.jsonData['id'], 110, "params 必须为字典")
            return False

        return True

    def jsonError(self, id, errno, errmsg):
        """
        处理错误信息
        :param id:
        :param errno:
        :param errmsg:
        :return:
        """
        # logging
        current_app.logger.warning("处理错误信息")
        self._response = {
            "jsonrpc": self.VERSION,
            "id": id,
            "error_code": errno,
            "errmsg": errmsg
        }


    def requireAuthentication(self, module, func):
        """
        不需要登陆也可以直接访问的白名单列表
        :param module:
        :param func:
        :return: True/False
        """
        b_list = ["user.login", "api.info", "reboot.error", "reboot.test"]

        # 方便测试
        # if "{}.{}".format(module, func) in b_list:
        #     return False
        # return True
        return False

    def callMethod(self, module, func, params, auth):
        """
        执行api调用
        :param module:
        :param func:
        :param params:
        :param auth:
        :return:
        """
        # 转换小写
        module_name = module.lower()
        func_name = func.lower()
        # 补充：去掉空格

        response = Response()
        at = AutoLoad()

        if not at.isValidModule(module_name):
            # logging
            current_app.logger.warning("{} 模块导入失败".format(module_name))
            response.errorCode = 120
            response.errorMessage = "模块加载失败，模块不存在"
            return response

        if not at.isValidMethod(func_name):
            # logging
            current_app.logger.warning("{} 函数验证失败".format(func_name))
            response.errorCode = 121
            response.errorMessage = "{} 模块下没有{} 这个方法".format(module_name, func_name)
            return response

        if self.requireAuthentication(module_name, func_name):
            # 需要登陆/需要验证
            if auth is None:
                # logging
                current_app.logger.warning("{}.{} 改操作需要提供token".format(module_name, func_name))

                response.errorCode = 122
                response.errorMessage = "该操作需要提供auth"
        try:
            called = at.getCallMethod()
            if callable(called):
                # response.data = called()
                response.data = called(**params)
            else:
                # logging
                current_app.logger.warning("{}.{} 不能被调用".format(module_name, func_name))
                response.errorCode = 123
                response.errorMessage = "{} 模块下的{}方法不能被执行".format(module_name, func_name)
        except Exception, e:
            # logging
            current_app.logger.warning("API 调用模块 {}.{} 执行中出错：{}".format(module, func, e.message))
            response.errorCode = -1
            response.errorMessage = e.message

        return response

    def processResult(self, response):
        """
        处理返回结果
        :param response:
        :return:
        """
        # logging
        current_app.logger.debug("处理执行后的结果")
        if response.errorCode != 0:
            self.jsonError(self.jsonData['id'],
                           response.errorCode,
                           response.errorMessage)
        else:
            self._response = {
                "jsonrpc": self.VERSION,
                "result": response.data,
                "id": self.jsonData['id']
            }


if __name__ == "__main__":
    # at = AutoLoad("idc.get")
    # at = AutoLoad()
    # at.isValidModule("idc")
    # at.isValidMethod("get")

    jr = JsonRpc()
    jr.jsonData = {
        "jsonrpc": 2.0,
        "method": "reboot.test",
        "id": 0,
        "auth": None,
        "params": {"name": "rock"}
    }
    ret = jr.execute()
    # print sys.stdout.encoding
    # reload(sys)  # reload 才能调用 setdefaultencoding 方法
    # sys.setdefaultencoding('utf-8')
    # print ret
    # print ret.get('errmsg', '')
    print json.dumps(ret, ensure_ascii=False)
