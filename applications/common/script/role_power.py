
from applications.extensions import db
from applications.models import User, Role, Power


def add_role_power():
    admin_powers = Power.query.filter(Power.id.in_(list(range(1, 20)))).all() # 1-20 号权限都插入给 主要管理员中 的 所有用户
    admin_user = Role.query.filter_by(id=1).first()
    for i in admin_powers:
        admin_user.power.append(i)

    # 额外插入数据
    admin_powers = Power.query.filter(Power.id.in_([16, 17, 18, 19, 20, 21])).all()
    admin_user = Role.query.filter_by(id=2).first()
    for i in admin_powers:
        admin_user.power.append(i)

    # 额外插入数据
    admin_powers = Power.query.filter(Power.id.in_([17,19])).all()
    admin_user = Role.query.filter_by(id=3).first()
    for i in admin_powers:
        admin_user.power.append(i)

    admin_powers = Power.query.filter(Power.id.in_([21])).all()
    admin_user = Role.query.filter_by(id=4).first()
    for i in admin_powers:
        admin_user.power.append(i)


    db.session.commit()
