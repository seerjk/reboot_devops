http://wiki.geekdream.com/Specification/json-rpc_2.0.html
JSON-RPC 2.0 规范(中文版)


@app.run(/api)
def api():
	jsondata = request.POST()
	jsonrpc = JsonRPC(jsondata)
	ret = jsonrpc.execute()
	return json.dumps(ret)
	
----------------------------------------------------------
class JsonRPC(object):
	def __init__(jsondata):
		self.jsondata = jsondata

	def execute():
		验证id
		验证jsondata
			通过：
				res = callMethod(module, fun, params, auth)
				self.processresult(res)
			不通过：
		
		return self.response
	
	def callMethod(module, fun, params, auth):
		res = Response()
		at = AutoLoad(module)
		
		at.isValidModule
			res.error_code = 10 #  接收返回值
			res.error_message = "模块不可用"  #  接收返回值
			return res
		
		at.isValidMethod()
			res.error_code = #  接收返回值
			res.error_message = #  接收返回值
			return res
		
		flag = requiresAuthentication()		# 判断module, func 是否需要登陆
		
		需要登陆：
			有没有token 
			验证权限
				失败： return res
		try:
			called = at.getCallMethod()
			res.data = called(**params)
		except Exception, e:
			res.error_code = 30
			res.error_message = e.message
		return res
	
	def processresult(response):
		如果error_code不为0
			jsonError()
		为0
			format = {
				“jsonrpc”: “2.0”, 
				“result”: response.data, 
				"id": 1
			}
			self.response = format
	
	def jsonError(id, errno, data=None):
		format_error = {
				“jsonrpc”: “2.0”, 
				“id”: 1
				"error_code" errno
				“errmsg”:data
		}
		self.response = format_error
	
	
	def validata():
		"""
		{
			 “jsonrpc”: “2.0”,
			“method”:“host.get”, 
			 “id”:1, 
			“auth”:None,
			“params”:{}
		}
		"""
		验证jsonrpc, 验证版本：2.0
		......(json里每一项都需要验证)
		
		不通过： 
			self.jsonError(id, errno, "jsonrpc版本不正确，应该为2.0")
			return False
		通过：return True
	
	def requiresAuthentication():
		idc.get  需要登陆  return True
		user.login 不需要登陆  return False
	

	
	
	
class AutoLoad(object):
	1 动态加载模块
	2 执行成功加载的模块
	# idc.get()
	
	def _load_module():
		加载模块
	
	def isValidMethod():
		验证模块下有没有指定方法
		有：return True
		没有： return False
		
	def isValidModule():
		验证模块是否存在（ls modules/idc.py）
		有：  import idc(这里会有导入失败)
			self.module
			return True
		没有：
			return False
	
	def getCallMethod():
		模块成功加载
		加载失败  return none
		加载成功  return idc.get()

class Response(object):
	data = None					# 执行后结果
	error_code = 0				# 错误
	error_message = None		#　错误信息
	

101  模块不存在
102  模块加载失败
103  指定模块下的函数不存在
104  jaonrpc版本不对，应该是2.0
