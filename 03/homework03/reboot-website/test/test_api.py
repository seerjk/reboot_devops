#!/usr/bin/python
# coding:utf-8
import requests
import json

url = "http://127.0.0.1:8000/api"

def test_api():
    header = {
        "content-type": "application/json"
        # "content-type": "application/jsonaa"
    }
    data = {
        "jsonrpc": 2.0,
        "method": "idc.create",
        "id": 0,
        "auth": None,
        "params": {
            "name": "yz",
            "idc_name": "北京亦庄机房",
            "address": "北京亦庄机房",
            "phone": "123456789",
            "email": "rock@51reboot.com",
            "user_interface": "rock",
            "user_phone": "123321123",
            "rel_cabinet_num": 50,
            "pact_cabinet_num": 60
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

"""
1. 代码抄写2遍以上
2. from flask import current_app 增加log处理功能

js
js  -- jquery
bootstrap
"""

def test_idc_get():
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


def test_idc_update():
    header = {
        "content-type": "application/json"
        # "content-type": "application/jsonaa"
    }
    data = {
        "jsonrpc": 2.0,
        "method": "idc.update",
        "id": 0,
        "auth": None,
        "params": {
            "data": {
                "rel_cabinet_num": 200
            },
            "where": {
                "id": "-1"
            }
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


def test_idc_delete():
    header = {
        "content-type": "application/json"
        # "content-type": "application/jsonaa"
    }
    data = {
        "jsonrpc": 2.0,
        "method": "idc.delete",
        "id": 0,
        "auth": None,
        "params": {
            "where": {
                "id": "4"
            }
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

if __name__ == "__main__":
    # test_api()
    # test_idc_get()
    # test_idc_update()
    test_idc_delete()