#!/usr/bin/env python
# coding:utf-8

import os
from app import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
# 导入Idc表
from app.models import Idc

# 设置config的模式 development
# 也可以从命令行 FLASK_CONFIG=development 设置
app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    # idc=Idc 要建立的Idc表
    return dict(app=app, db=db, idc=Idc)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

# $ python manage.py runserver -h 0.0.0.0 -p 8000
