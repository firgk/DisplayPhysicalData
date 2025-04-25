from applications.models import User, Role, Power
import datetime
now_time = datetime.datetime.now()



userdata = [
    User(
        id=1,
        username='admin',
        password_hash='pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85',
        create_at=now_time,
        enable=1,
        realname='校级领导',
        remark=' ',
        avatar='/static/system/admin/images/avatar.jpg',
    ),
    User(
        id=2,
        username='dean',
        password_hash='pbkdf2:sha256:150000$cRS8bYNh$adb57e64d929863cf159f924f74d0634f1fecc46dba749f1bfaca03da6d2e3ac',
        create_at=now_time,
        enable=1,
        realname='教学管理部门',
        remark=' ',
        avatar='/static/system/admin/images/avatar.jpg',
    ),
    User(
        id=3,
        username='input',
        password_hash='pbkdf2:sha256:150000$skME1obT$6a2c20cd29f89d7d2f21d9e373a7e3445f70ebce3ef1c3a555e42a7d17170b37',
        create_at=now_time,
        enable=1,
        realname='负责成绩录入的教师',
        remark=' ',
        avatar='/static/system/admin/images/avatar.jpg',
    ),
    User(
        id=4,
        username='show',
        password_hash='pbkdf2:sha256:150000$skME1obT$6a2c20cd29f89d7d2f21d9e373a7e3445f70ebce3ef1c3a555e42a7d17170b37',
        create_at=now_time,
        enable=1,
        realname='大屏展示1',
        remark=' ',
        avatar='/static/system/admin/images/avatar.jpg',
    ),
]

