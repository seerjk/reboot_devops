#!/usr/bin/env python
# coding:utf-8

import os
from app import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

# $ python manage.py runserver -h 0.0.0.0 -p 8000
