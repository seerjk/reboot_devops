# coding:utf-8

# 1 所有的结果直接返回
# 2 error, try-except  raise Exception

def test(**kwargs):
    # print kwargs
    return kwargs
    # return "reboot test hahaha"


def error(**kwargs):
    raise Exception("执行过程中出现错误")

if __name__ == "__main__":
    k = {"name": "rock"}
    print test(**k)