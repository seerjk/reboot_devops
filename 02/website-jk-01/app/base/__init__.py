# /usr/bin/python
# coding:utf-8

import os
import imp

class AutoLoad():
    """
    自动加载模块类
    """
    def __init__(self):
        # 指定项目自动加载模块的目录
        DIR = os.path.abspath(os.path.dirname(__file__))
        self.modules_dir = os.path.join(DIR, "..", "modules")
        # print self.modules_dir
        self.modules_dir = os.path.abspath(self.modules_dir)
        # print DIR
        # print self.modules_dir

        # idc.get
        self.module_name = ""             # 模块名
        self.func = ""                    # 函数名
        self.module = None                # 已加载的模块

    def isValidModule(self, module_name):
        """
        验证模块是否可用
        :param module_name: 需要导入的模块名
        :return: True / False
        """
        self.module_name = module_name
        return  self._load_module()


    def isValidMethod(self, func):
        """
        验证函数是否可用
        :param func: 函数名
        :return: True/False
        """
        self.func = func
        if self.module is None:
            return False
        return hasattr(self.module, self.func)


    def getCallMethod(self):
        """
        返回可执行的函数
        :return: func / None
        """
        if hasattr(self.module, self.func):
            return getattr(self.module, self.func, None)
        return None


    def _load_module(self):
        """
        动态加载模块
        :return:
        """
        ret = False
        # 列出模块目录下所有的文件 ls modules
        for file_name in os.listdir(self.modules_dir):
            # 遍历模块目录下的所有文件
            if file_name.endswith(".py"):
                # 如果文件名是以.py结尾
                # 从文件名中取出模块名
                module_name = file_name.rstrip(".py")
                # print module_name

                if module_name == self.module_name:
                    # 当前遍历的这个py文件是我们想要导入的py文件
                    fp, pathname, desc = imp.find_module(module_name, [self.modules_dir])
                    if not fp:
                        continue

                    try:
                        self.module = imp.load_module(module_name, fp, pathname, desc)
                        ret = True
                    except Exception:
                        pass
                    finally:
                        fp.close()
                    break

        return ret


if __name__ == "__main__":
    at = AutoLoad()
    # at = AutoLoad("idc.get")
    # at.module_name = "idc"
    # at.func = "get"

    # at.isValidModule("idc")
    # at.isValidMethod("get")
    print at.isValidModule("reboot11")