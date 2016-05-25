#!/usr/bin/python
# coding:utf-8
import requests
import json

url = "http://10.1.1.71:8000/api"

def test_api():
    header = {
        "content-type": "application/json"
    }
    data = {
        "jsonrpc": 2.0,
        "method": "reboot.test",
        "id": 0,
        "auth": None,
        "params": {
            "name": "rock abcdedf"
        }
    }
    # r = requests.get(url, headers=header, params=json.dumps(data))
    r = requests.post(url, headers=header, data=json.dumps(data))
    print r.status_code
    print r.content

"""
1. 代码抄写2遍以上
2. from flask import current_app 增加log处理功能

js
js  -- jquery
bootstrap
"""

if __name__ == "__main__":
    test_api()