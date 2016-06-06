#!/usr/bin/python
# coding:utf-8

import requests
import json
import ast


def zabbix_api(data):
    url = "http://192.168.99.14/zabbix/api_jsonrpc.php"

    header = {"Content-Type": "application/json-rpc"}

    r = requests.post(url, data=json.dumps(data), headers=header)

    # print r.status_code
    # print r.content
    return ast.literal_eval(r.content)
# data = {
#             "jsonrpc": "2.0",
#             "method": "apiinfo.version",
#             "id": 1,
#             "auth": None,
#             "params": {}
# }

if __name__ == "__main__":
    # login:
    login_data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "zabbix"
        },
        "id": 1,
        "auth": None
    }
    ret = zabbix_api(login_data)
    # print ret
    # print type(ret)
    # exit(0)
    token = ret['result']

    # host.get

    get_host_data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid"],
            "selectParentTemplates": [
                "templateid",
                "name"
            ],
        },
        "id": 2,
        "auth": token
    }
    print zabbix_api(get_host_data)

    get_hostgroup_data = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
        },
        "auth": token,
        "id": 3
    }
    # print zabbix_api(get_hostgroup_data)

    get_template_data = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
        },
        "auth": token,
        "id": 4
    }

    # print zabbix_api(get_template_data)

    # create host
    host_create_data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "reboot-ms-web-01",
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": "192.168.99.11",
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": "2"
                }
            ],
            "inventory_mode": 0,
            "inventory": {
                "macaddress_a": "080027",
                "macaddress_b": "95952d"
            }
        },
        "auth": token,
        "id": 3
    }
    # print zabbix_api(host_create_data)

    # update host with a template
    host_update_data = {
        "jsonrpc": "2.0",
        "method": "host.update",
        "params": {
            "hostid": "10107",
            "templates": [
                {
                    "templateid": "10102"
                }
            ]
        },
        "auth": token,
        "id": 6
    }
    # print zabbix_api(host_update_data)



