from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role
from applications.models import User, AdminLog,College,Student

bp = Blueprint('front', __name__, url_prefix='/front')


# 此处修改需要和 /system/index 下同步
# 此处不需要更改
@bp.get('/main/')
@login_required
def index():
    student = current_user
    college_info = College.query.filter_by(collegeCode=student.collegeCode).first()
    student.collegeCode=college_info.className
    return render_template('front/index.html', user=student)






