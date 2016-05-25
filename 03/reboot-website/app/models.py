#!/usr/bin/env python
# coding:utf-8
from app import db

class Idc(db.Model):
    # 表名
    __tablename__     = "idc"
    id               = db.Column(db.Integer, primary_key=True)
    # IDC字母检查
    name             = db.Column(db.String(50), index=True, nullable=False, unique=True)
    # IDC中午名称
    idc_name         = db.Column(db.String(50), nullable=False)
    # IDC详细地址
    address          = db.Column(db.String(255), nullable=False)
    # 客服电话
    phone            = db.Column(db.String(20), nullable=False)
    # 客服邮件
    email            = db.Column(db.String(50), nullable=False)
    # IDC接口人
    user_interface   = db.Column(db.String(50), nullable=False)
    # IDC接口人 电话
    user_phone       = db.Column(db.String(20),nullable=False)
    # 实际机柜数
    rel_cabinet_num  = db.Column(db.Integer, nullable=False)
    # 合同机柜数
    pact_cabinet_num = db.Column(db.Integer, nullable=False)
