#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from flask import request
from app.base import JsonRpc
from . import main
import json
from flask import current_app

@main.route('/', methods=['GET','POST'])
def index():
    return 'index'

@main.route("/api", methods=['GET', 'POST'])
def api():
    # application/json
    # application/json-rpc
    allowed_content = ["application/json", "application/json-rpc"]

    # if request.content_type in allowed_content:
    #     jsonData = request.get_json()
    #     print jsonData
    #     print type(jsonData)
    if True:
        jsonData = request.get_json()
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        ret = jsonrpc.execute()
        return json.dumps(ret, ensure_ascii=False)
    else:
        return "200", 400
    # print request.content_type

