

# 调用者 flask 页面

@app.run(/api)
def api():
    # return "hello world."
    jsondata = request.POST()
    jsonrpc = JsonRPC(jsondata)
    ret = jsonrpc.execute()
    return json.dumps(net)


# ----------------------------------------------
class JsonRPC(object):

    def __init__(jsondata):
        self.jsondata = jsondata

    def execute():
        '''
        验证id
        验证jsondata
            通过：
                callMethod(module, func, params, auth)
            不通过：
        '''
        return self.response

    def callMethod(module, func, params):
        res = Response()
        at = AutoLoad(module)

        at.isValidModule()
            res.error_code = 10
            res.error_message = "模块不可用"
            return res
        
        at.isValidMethod()
            res.error_code = 11
            res.error_message = "方法不可用"
            return res

        flag = requireAuthentication()  # 判断module, func是否需要登陆。

        if 需要登陆:
            有没有 token 

            验证token 的权限
            # 要权限验证接口
                失败：
                    res.error_code = 12
                    res.error_message = "方法不可用"
                    return res
        else
            不需要登陆


        try:
            called = at.getCallMethod()
            执行 idc.get aaa bbb 一个名字
            res.data = called(**params)
            # 无异常，处理结果
            self.process_result(data)
        except Exception, e:
            # errormsg
            res.error_code = 30
            res.error_message = e.message
            return res

    def process_result(response):
        # 处理要返回的结果
        # 如果error_code 不为0，有错误
        # 执行过程有问题
        json_error(id, errno, data)

        # 如果error_code 为0
        执行过程没有问题
        format = {
            "jsonrpc": "2.0",
            "result": response.data,
            "id": 1
        }
        self.response = format

    def json_error(id, errno, data=None):
        format_error = {
            "jsonrpc": "2.0",
            "id": 1,
            "error_code": errno,
            "errmsg": data
        }
        self.response = format_error



    def validdata():
        # valid_jsondata
        逐行验证
        '''
        {
            "jsonrpc": "2.0",
            "method": "idc.get",
            "id": 1,
            "auth": None,
            "params": {}
        }
        '''
        # 验证jsondata ppt中的json格式
        验证jsonrpc（是否有字段），验证版本：是否2.0
        # .... (json里的每一项都需要验证)

        通过：
        return True

        不通过：
        self.json_error(id, errno, "jsonrpc版本不正确，应该为2.0")
        return False

    def requireAuthentication():
        idc.get  需要登陆 return True
        user.login 不需要登陆 return False

class AutoLoad(object):
    '''
    功能：
    1.动态加载模块
        为什么要动态加载？
        静态加载所有模块，如果中途有新加的模块，需要重启服务才能生效。
        动态加载可以不重启服务。
    2.执行成功加载的模块
    idc.py -- idc.get() 遍历目录下所有文件，存在则尝试 import 导入
    '''
    def _load_module():
        '''
        加载模块
        '''
        isValidModule()
        加载

        pass

    def getCallMethod():
        '''
        模块成功加载
        如果模块成功加载，返回模块的方法
            加载成功，return idc.get()
        如果加载失败，return None
        '''
        pass

    def isValidMethod():
        '''
        验证模块下有没有指定方法
        hasattr
        有：  return True
        没有：return False
        '''
        pass

    def isValidModule():
        '''
        验证模块是否存在
        指定目录ls一下，看是否有 idc.py文件
        ```
            ls modules/idc.py
            In [1]: import os

            In [2]: os.listdir("./")
            Out[2]: ['devops_note01.md', 'main.py', 'arch.gliffy', 'api_intro.gliffy', 'api.py']
        ```
        
        有：
            尝试import idc (这里会有导入失败)
            self.module 保存模块
            return True
        没有：
            return False
        '''
        pass


# 前期先忽略auth，认为登陆后都有权限。

class Response(object):
    # 返回数据
    data = None             # 执行后的结果
    error_code = 0          # 错误编号，错误才有，正确的省去
    error_message = None    # 具体的错误信息



* 维护配置文件，说一下动态加载模块
或者可以放在配置文件中，定时扫描配置文件，来实现动态加载模块
如zabbix
{
    idc: [get, create, update, delete]
    server: [get, create, update, delete]
}

* 每次需要用这个模块用_load_module()动态加载，如果频繁加载，会不会造成很大的开销？
每次请求来，都会扫描一次，造成I/O开销很大。
定时扫描磁盘后，可以存入缓存(redis,memcache)，如1小时内不扫描磁盘了。
优点：后续加载快
缺点：新模块生效慢
密码访问量很大，可以用缓存 