#!/usr/bin/python
# coding:utf-8

from __future__ import unicode_literals
from flask import render_template, request
import json
from . import main
import app.utils
import json
from app.utils import jump

"""
IDC 列表页面
"""
@main.route("/resources/idc/", methods=["GET"])
def resources_idc():
    ret = app.utils.api_action("idc.get", {"where": {"status": 1}})
    # print ret
    return render_template("resources/server_idc_list.html",
                           title="IDC信息",
                           show_resource=True,
                           show_idc_list=True,
                           idcs=ret)

@main.route("/resources/idc/list", methods=["POST"])
def resources_idc_list():
    ret = app.utils.api_action("idc.get")
    return json.dumps(ret)

"""
修改IDC信息
"""
@main.route("/resources/idc/modify/<int:idc_id>", methods=["GET"])
def resources_idc_modify(idc_id):
    ret = app.utils.api_action("idc.get", {"where": {"id": idc_id}})
    if ret:
        return render_template("resources/server_idc_modify.html",
                               title="修改IDC信息",
                               idc=ret[0])
    return render_template("404.html"), 404


@main.route("/resources/idc/update", methods=["POST"])
def resources_idc_update():
    data = request.form.to_dict()
    id = data.pop("id")
    ret = app.utils.api_action("idc.update",
                               {
                                   "data": data,
                                   "where": {"id": id}
                               })

    if ret:
        return render_template("public/success.html",
                               next_url="/resources/idc/")
    else:
        return render_template("public/error.html",
                               next_url="/resources/idc/")


"""
添加IDC
"""
@main.route("/resources/idc/add/", methods=["GET"])
def resources_add_idc():
    return render_template("resources/server_add_idc.html",
                           title="添加IDC信息",
                           show_resource=True,
                           show_idc_list=True)

"""
执行添加idc
"""
@main.route("/resources/idc/doadd/", methods=["POST"])
def resources_doadd_idc():
    params = request.form.to_dict()
    # print data
    ret = app.utils.api_action("idc.create", params)
    # print ret

    if ret:
        return render_template("public/success.html",
                               next_url="/resources/idc/",
                               title="操作成功"
                               )
    else:
        return render_template("public/error.html",
                               next_url="/resources/idc/",
                               title="操作失败"
                               )


"""
删除IDC
"""
# @main.route("/resources/idc/dodelete", methods=["GET"])
# def resources_dodelete_idc():
#     id = request.args.get("id")
#
#     ret = app.utils.api_action("idc.delete",
#                                {
#                                    "where": {"id": id}
#                                })
#     if ret:
#         return "ok"
#     else:
#         return "error"

@main.route("/resources/idc/delete/", methods=["POST"])
def resources_delete_idc():
    id = request.form.get("id", 0)
    # print "#### ID:", id
    # return "0"
    # return "1"
    ret = app.utils.api_action("idc.update",
                             {
                                 "where": {"id": id},
                                 "data": {"status": 0}
                             })
    return str(ret)

"""
服务器列表页面
"""
@main.route("/resources/server/list/", methods=["GET"])
def resources_server_list():
    # 获取server信息
    servers = app.utils.api_action("server.get")
    return render_template("resources/server_list.html",
                           title="服务器信息",
                           servers=servers)

"""
添加服务器
"""
@main.route("/resources/server/add/", methods=["GET"])
def resources_server_add():
    # 获取制造商信息
    manufacturers = app.utils.api_action("manufacturers.get")

    # 获取服务器类型信息
    products = app.utils.api_action("product.get", {"where": {"pid": 0}})

    # 获取服务器状态信息
    status = app.utils.api_action("status.get")

    # 获取IDC信息
    idc_info = app.utils.api_action("idc.get", {"output": ["name", "id"]})

    # 获取电源功率信息
    powers = app.utils.api_action("power.get")

    # 获取raid信息
    raids = app.utils.api_action("raid.get")

    # 获取RAID型号信息
    raidtypes = app.utils.api_action("raidtype.get")

    # 获取远程管理卡信息
    managementcardtypes = app.utils.api_action("managementcard.get")

    # 获取供应商信息
    suppliers = app.utils.api_action("supplier.get")

    return render_template("resources/server_add.html",
                           title="添加服务器",
                           manufacturers=manufacturers,
                           products=products,
                           status=status,
                           idc_info=idc_info,
                           powers=powers,
                           raids=raids,
                           raidtypes=raidtypes,
                           managementcardtypes=managementcardtypes,
                           suppliers=suppliers
                           )

"""
执行添加服务器
"""
@main.route("/resources/server/doadd/", methods=["POST"])
def resources_server_doadd():
    params = request.form.to_dict()
    print params
    ret = app.utils.api_action("server.create", params)
    jump_url = "/resources/server/add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
修改服务器信息
/resources/server/modify/1
"""


"""
添加制造商
"""
@main.route("/resources/manufacturers/add/", methods=["GET"])
def resources_manufacturers_add():
    return render_template("resources/server_add_manufacturers.html",
                           title="添加制造商")


"""
执行添加制造商
"""
@main.route("/resources/server/manufacturers/doadd/", methods=["POST"])
def resources_manufacturers_doadd():
    params = request.form.to_dict()
    print params
    ret = app.utils.api_action("manufacturers.create", params)
    jump_url = "/resources/manufacturers/add/"
    # if ret:
    #     return render_template("public/success.html",
    #                            next_url="/resources/manufacturers/add/")
    # else:
    #     return render_template("public/error.html",
    #                            next_url="/resources/manufacturers/add/")
    return app.utils.jump(ret, jump_url, jump_url)

"""
添加服务器类型
"""
@main.route("/resources/server_servertype_add/", methods=["GET"])
def resources_servertype_add():
    manufacturers = app.utils.api_action("manufacturers.get")
    return render_template("resources/server_add_servertype.html",
                           title="添加服务器类型",
                           manufacturers=manufacturers)

"""
执行添加服务器类型
"""
@main.route("/resources/server_servertype_doadd/", methods=["POST"])
def resources_servertype_doadd():
    params = request.form.to_dict()
    # print params
    jump_url = "/resources/server_servertype_add/"
    ret = app.utils.api_action("servertype.create", params)
    # if ret:
    #     return render_template("public/success.html",
    #                            next_url="/resources/server_servertype_add/")
    # else:
    #     return render_template("public/error.html",
    #                            next_url="/resources/server_servertype_add/")
    return app.utils.jump(ret, jump_url, jump_url)


"""
添加业务线或产品线
"""
@main.route("/resources/server_product_add/", methods=["GET"])
def resources_server_product_add():
    products = app.utils.api_action("product.get")
    return render_template("resources/server_add_product.html",
                           products=products)


"""
执行添加业务线或产品线
"""
@main.route("/resources/server_product_doadd/", methods=["POST"])
def resources_server_product_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("product.create", params)
    jump_url = "/resources/server_product_add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加服务器状态
"""
@main.route("/resources/status/add/", methods=["GET"])
def resources_server_status_add():
    return render_template("resources/server_add_status.html")


"""
执行添加服务器状态
"""
@main.route("/resources/status/doadd/", methods=["POST"])
def resources_server_status_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("status.create", params)
    jump_url = "/resources/status/add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加机柜
"""
@main.route("/resources/cabinet/add/", methods=["GET"])
def resources_server_cabinet_add():
    idcs = app.utils.api_action("idc.get", {"output": ["name"]})
    powers = app.utils.api_action("power.get")
    return render_template("resources/server_add_cabinet.html",
                           idcs=idcs,
                           powers=powers)


"""
执行添加机柜
"""
@main.route("/resources/cabinet/doadd/", methods=["POST"])
def resources_server_cabinet_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("cabinet.create", params)
    jump_url = "/resources/status/add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加电源功率
"""
@main.route("/resources/power/add/", methods=["GET"])
def resources_server_power_add():
    return render_template("resources/server_add_power.html")


"""
执行添加电源功率
"""
@main.route("/resources/power/doadd/", methods=["POST"])
def resources_server_power_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("power.create", params)
    jump_url = "/resources/power/add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加raid
"""
@main.route("/resources/server_raid_add/", methods=["GET"])
def resources_server_raid_add():
    return render_template("resources/server_add_raid.html")


"""
执行添加raid
"""
@main.route("/resources/server_raid_doadd/", methods=["POST"])
def resources_server_raid_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("raid.create", params)
    jump_url = "/resources/server_raid_add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加RAID型号
"""
@main.route("/resources/server_raidcardtype_add/", methods=["GET"])
def resources_server_raidcardtype_add():
    return render_template("resources/server_add_raidcardtype.html")


"""
执行添加RAID型号
"""
@main.route("/resources/server_raidcardtype_doadd/", methods=["POST"])
def resources_server_raidcardtype_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("raidtype.create", params)
    jump_url = "/resources/server_raidcardtype_add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加远程管理卡
"""
@main.route("/resources/server_managementcardtype_add/", methods=["GET"])
def resources_server_managementcard_add():
    return render_template("resources/server_add_managementcardtype.html")


"""
执行添加远程管理卡
"""
@main.route("/resources/server_managementcardtype_doadd/", methods=["POST"])
def resources_server_managementcard_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("managementcard.create", params)
    jump_url = "/resources/server_managementcardtype_add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
添加供应商
"""
@main.route("/resources/server_supplier_add/", methods=["GET"])
def resources_server_supplier_add():
    return render_template("resources/server_add_supplier.html")


"""
执行添加供应商
"""
@main.route("/resources/server_supplier_doadd/", methods=["POST"])
def resources_server_supplier_doadd():
    params = request.form.to_dict()
    ret = app.utils.api_action("supplier.create", params)
    jump_url = "/resources/server_supplier_add/"

    return app.utils.jump(ret, jump_url, jump_url)


"""
    ajax 操作
    根据制造商，获取服务器类型
    http://127.0.0.1:8000/resources/ajax/get_server_type?manufacturers_id=2
"""
@main.route("/resources/ajax/get_server_type", methods=["GET"])
def resrouce_ajax_get_servertype():
    params = request.args.to_dict()
    if params:
        servertypes = app.utils.api_action("servertype.get",
                                           {"where": params})
        return json.dumps(servertypes)
    return ""

"""
    ajax 操作
    根据一级业务线，获取二级业务线
"""
@main.route("/resources/ajax/get_server_product/", methods=["GET"])
def resources_ajax_get_product():
    params = request.args.to_dict()
    if params:
        data = app.utils.api_action("product.get",
                                    {
                                        "output": ["id", "service_name", "pid"],
                                        "where": params
                                    })
        return json.dumps(data)
    return ""


"""
    ajax 操作
    根据idc信息，获取该idc下的所有机柜信息
"""
@main.route("/resources/ajax/get_cabinet/", methods=["GET"])
def resources_ajax_get_cabinet():
    params = request.args.to_dict()
    if params:
        cabinets = app.utils.api_action("cabinet.get",
                                        {
                                            "output": ["id", "name"],
                                            "where": params
                                        })
        return json.dumps(cabinets)
    return ""