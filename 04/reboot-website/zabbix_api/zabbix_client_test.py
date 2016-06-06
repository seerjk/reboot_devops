#!/usr/bin/python
# coding: utf-8

from zabbix_client import ZabbixServerProxy

def host_test():
    s = ZabbixServerProxy('http://192.168.99.14/zabbix')
    s.user.login(user='Admin', password='zabbix')

    # create hostgroup reboot
    # print s.hostgroup.create(name="reboot")

    # get groupid
    reboot_groupid = s.hostgroup.get(output=['groupid'], filter={"name": "reboot"})[0]['groupid']

    # print reboot_groupid
    # print type(reboot_groupid)

    hosts_list = [
        {"ip": "172.16.31.12", "host": "yz-ms-web-01"},
        {"ip": "172.16.31.13", "host": "yz-ms-web-02"},
        {"ip": "172.16.31.14", "host": "yz-ms-web-03"},
        {"ip": "172.16.31.15", "host": "yz-ms-web-04"},
        {"ip": "172.16.31.16", "host": "yz-ms-web-05"}
    ]

    # 批量创建主机，并加入到reboot组
    # for host in hosts_list:
    #     print s.host.create(
    #         host=host['host'],
    #         interfaces=[
    #             {
    #                 "ip": host['ip'],
    #                 "type": 1,
    #                 "main": 1,
    #                 "useip": 1,
    #                 "dns": "",
    #                 "port": "10050"
    #             }
    #         ],
    #         groups=[
    #             {"groupid": reboot_groupid}
    #         ]
    #     )

    # 将这些机器加上 Template OS Linux 这个模板
    template_id = s.template.get(
        output=['templateid'],
        filter={
            "host": ["Template OS Linux"]
        })[0]['templateid']
    print template_id

    for host in hosts_list:
        host_id = s.host.get(
            output=['hostid'],
            filter={
                "host": host['host']
            })[0]['hostid']
        print host_id
        print s.host.update(
            hostid=host_id,
            templates=[
                {"templateid": template_id}
            ]
        )

def network_device_test():
    s = ZabbixServerProxy('http://192.168.99.14/zabbix')
    s.user.login(user='Admin', password='zabbix')

    
    pass

if __name__ == "__main__":
    network_device_test()


