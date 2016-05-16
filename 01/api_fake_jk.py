# api_fake_jk.py

# 流程
接收api request
验证 json数据有效性
验证权限
动态加载
    验证模块
    验证方法
执行方法
response返回数据


class JsonRPC(object):
    pass


class AutoLoad(object):
    '''
    动态加载模块
    1. 验证模块：验证模块是否存在
    2. 验证方法：验证模块下是否有该方法
    3. 动态加载模块：import
    4. 调用方法
    '''


class ResponseData(object):
    # 定义返回的数据，没有方法
    data = None             # 执行后的结果
    error_code = 0          # 错误编号，错误才有，正确的省去
    error_message = None    # 具体的错误信息

预先：
错误代码定义
101 模块不存在
102 模块加载失败
103 指定模块下的函数方法不存在
104 jsonrpc版本不对，应该是2.0

错误日志