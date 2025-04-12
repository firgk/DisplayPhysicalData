import datetime

from flask.cli import AppGroup

from applications.extensions import db
from applications.models import User, Role, Power
from applications.common.script.student import datas
from applications.common.script.userdata import userdata
from applications.common.script.college import colleges
from applications.common.script.roledata import roledata
from applications.common.script.powerdata import powerdata
from applications.common.script.user_role import add_user_role
from applications.common.script.role_power import add_role_power



admin_cli = AppGroup("admin")
now_time = datetime.datetime.now()




@admin_cli.command("init")
def init_db():
    db.session.add_all(userdata)
    print("加载系统必须用户数据")
    db.session.add_all(roledata)
    print("加载系统必须角色数据")
    db.session.add_all(datas)
    print("加载 student datas")
    db.session.add_all(colleges)
    print("加载 student colleges")


    db.session.add_all(powerdata)

    print("加载系统必须权限数据")
    db.session.commit()

    add_user_role()
    print("用户-角色数据存入")
    add_role_power()
    print("角色-权限数据存入")


    print("数据初始化完成，请使用run脚本运行")
