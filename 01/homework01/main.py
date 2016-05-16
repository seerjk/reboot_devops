# coding:utf-8
import os


class AutoLoad(object):
    def __init__(module_name):
        self.module_name = module_name
        status = is_valid_module()
        if status == 0:
            return 0
        else:
            return status

    def is_valid_module():
        '''
        验证模块是否存在
        '''
        modules_list = os.listdir("./modules/")
        if self.module_name + '.py' in modules_list:
            try:
                load_module()
            except Exception e:
                # 模块加载失败
                return 102
        else:
            # 模块不存在
            return 101
        return 0



    def load_module():
        exec("import modules.%s as %s" % (self.module_name, self.module_name))



class Response(object):
    '''
    返回数据类，
    data 返回结果，如果报错则返回None
    error_code 错误代码，如果无错误，返回0
    error_message 错误信息，

    error_code:
        101  模块不存在
        102  模块加载失败
        103  指定模块下的函数不存在
        104  jaonrpc版本不对，应该是2.0
    '''
    data = None
    error_code = 0
    error_message= None


def main():
    pass


if __name__ == "__main__":
    main()
