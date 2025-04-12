from flask import Blueprint, render_template,jsonify
from flask_login import login_required, current_user
from applications.extensions import db
from applications.models import Student
from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role
from applications.models import User, AdminLog



bp = Blueprint('api', __name__, url_prefix='/api')



@bp.get('/')
@login_required  # 如果需要用户登录，取消注释
def score():

    scores = db.session.query(Score).all()

    # 模拟对成绩进行分组统计，这里以 allScore 为例
    score_ranges = {
        "0 分以上": 0,
        "20 - 29 分": 0,
        "30 - 39 分": 0,
        "40 - 49 分": 0,
        "50 分以上": 0
    }

    for student in scores:
        try:
            score = float(student.allScore)
            if score < 20:
                score_ranges["20 分以xia "] += 1
            elif 20 <= score < 30:
                score_ranges["20 - 29 分"] += 1
            elif 30 <= score < 40:
                score_ranges["30 - 39 分"] += 1
            elif 40 <= score < 50:
                score_ranges["40 - 49 分"] += 1
            else:
                score_ranges["50 分以上"] += 1
        except (ValueError, TypeError):
            continue

    echarts_data = [{"value": value, "name": name} for name, value in score_ranges.items()]

    return {
        "data": echarts_data,
        "count": len(scores)
    }