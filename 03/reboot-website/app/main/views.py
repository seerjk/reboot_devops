#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from flask import request, render_template
from app.base import JsonRpc
from . import main
import json
from flask import current_app


@main.route('/', methods=['GET','POST'])
def index():
    # current_app 其实就是app
    current_app.logger.debug("访问首页")
    return 'index'

@main.route("/dashboard/", methods=["GET"])
def dashboard():
    return render_template("/static/dashboard.html")


@main.route("/api", methods=['GET', 'POST'])
def api():
    # application/json
    # application/json-rpc
    allowed_content = ["application/json", "application/json-rpc"]

    # if request.content_type in allowed_content:
    #     jsonData = request.get_json()
    #     print jsonData
    #     print type(jsonData)
    if request.content_type in allowed_content:
        jsonData = request.get_json()
        current_app.logger.debug("请求的json数据为：{}".format(json.dumps(jsonData)))
        jsonrpc = JsonRpc()
        jsonrpc.jsonData = jsonData
        ret = jsonrpc.execute()
        return json.dumps(ret, ensure_ascii=False, encoding='utf-8')
    else:
        current_app.logger.debug(
            "用户请求的content_type为：{}，不予处理".format(request.content_type))
        return "200", 400
    # print request.content_type

