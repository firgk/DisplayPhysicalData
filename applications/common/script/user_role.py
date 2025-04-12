
from applications.extensions import db
from applications.models import User, Role, Power

def add_user_role():
    admin_role = Role.query.filter_by(id=1).first()
    admin_user = User.query.filter_by(id=1).first()
    admin_user.role.append(admin_role)
    test_role = Role.query.filter_by(id=2).first()
    test_user = User.query.filter_by(id=2).first()
    test_user.role.append(test_role)
    test_role = Role.query.filter_by(id=3).first()
    test_user = User.query.filter_by(id=3).first()
    test_user.role.append(test_role)
    test_role = Role.query.filter_by(id=4).first()
    test_user = User.query.filter_by(id=4).first()
    test_user.role.append(test_role)
    db.session.commit()

