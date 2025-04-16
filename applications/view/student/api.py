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
from applications.models import User, AdminLog,Student,College



bp = Blueprint('api', __name__, url_prefix='/api')


@bp.get('/distribution_of_actual_test_scores')
@login_required  # 如果需要用户登录，取消注释
def distribution_of_actual_test_scores():

    students = db.session.query(Student).all()

    # 模拟对成绩进行分组统计，这里以 allScore 为例
    score_ranges = {
        "0 分以上": 0,
        "20 - 29 分": 0,
        "30 - 39 分": 0,
        "40 - 49 分": 0,
        "50 分以上": 0
    }

    for student in students:
        try:
            score = float(student.score_allScore)
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
        "count": len(students)
    }



# /api/average_bmi_data 接口
# 计算 各年级平均BMI
@bp.get('/average_bmi_data')
@login_required  # 如果需要用户登录，取消注释
def average_bmi_data():
    # 获取所有学生数据
    students = db.session.query(Student).all()
    
    # 初始化各年级的数据统计
    grade_data = {
        '1': {'bmi': [], 'weight': [], 'height': []},  # 大一
        '2': {'bmi': [], 'weight': [], 'height': []},  # 大二
        '3': {'bmi': [], 'weight': [], 'height': []},  # 大三
        '4': {'bmi': [], 'weight': [], 'height': []}   # 大四
    }
    
    # 遍历学生数据，按年级分类
    for student in students:
        try:
            grade = student.grade
            if grade not in grade_data:
                continue
                
            # 尝试转换身高和体重为浮点数
            height = float(student.sHeight) if student.sHeight else None
            weight = float(student.sWeight) if student.sWeight else None
            
            if height and weight:
                # 计算BMI (体重(kg) / 身高(m)^2)
                bmi = weight / ((height/100) ** 2)
                grade_data[grade]['bmi'].append(bmi)
                grade_data[grade]['weight'].append(weight)
                grade_data[grade]['height'].append(height)
        except (ValueError, TypeError, ZeroDivisionError):
            continue
    
    # 计算各年级的平均值
    result = {
        'bmi': [],
        'weight': [],
        'height': []
    }
    
    # 按年级顺序（大一到大四）计算平均值
    for grade in ['1', '2', '3', '4']:
        data = grade_data[grade]
        
        # 计算BMI平均值
        avg_bmi = sum(data['bmi']) / len(data['bmi']) if data['bmi'] else 0
        result['bmi'].append(round(avg_bmi, 2))
        
        # 计算体重平均值
        avg_weight = sum(data['weight']) / len(data['weight']) if data['weight'] else 0
        result['weight'].append(round(avg_weight, 2))
        
        # 计算身高平均值
        avg_height = sum(data['height']) / len(data['height']) if data['height'] else 0
        result['height'].append(round(avg_height, 2))
    
    return jsonify({
        'data': result
    })


@bp.get('/grade_score_distribution')
@login_required
def grade_score_distribution():
    # 获取所有学生数据
    students = db.session.query(Student).all()
    
    # 初始化各年级的成绩统计
    grade_data = {
        '1': {'优秀': 0, '良好': 0, '及格': 0, '不及格': 0},  # 大一
        '2': {'优秀': 0, '良好': 0, '及格': 0, '不及格': 0},  # 大二
        '3': {'优秀': 0, '良好': 0, '及格': 0, '不及格': 0},  # 大三
        '4': {'优秀': 0, '良好': 0, '及格': 0, '不及格': 0}   # 大四
    }
    
    # 遍历学生数据，按年级和成绩等级分类
    for student in students:
        try:
            grade = student.grade
            if grade not in grade_data:
                continue
                
            # 尝试转换总成绩为浮点数
            score = float(student.score_allScore) if student.score_allScore else 0
            
            # 根据成绩划分等级
            if score >= 90:
                grade_data[grade]['优秀'] += 1
            elif score >= 80:
                grade_data[grade]['良好'] += 1
            elif score >= 60:
                grade_data[grade]['及格'] += 1
            else:
                grade_data[grade]['不及格'] += 1
        except (ValueError, TypeError):
            continue
    
    # 格式化数据为前端需要的格式
    result = {
        '优秀': [],
        '良好': [],
        '及格': [],
        '不及格': []
    }
    
    # 按年级顺序（大一到大四）整理数据
    for grade in ['1', '2', '3', '4']:
        data = grade_data[grade]
        result['优秀'].append(data['优秀'])
        result['良好'].append(data['良好'])
        result['及格'].append(data['及格'])
        result['不及格'].append(data['不及格'])
    
    return jsonify({
        'data': result
    })


@bp.get('/completion_statistics')
@login_required
def completion_statistics():
    # 获取所有学生数据
    students = db.session.query(Student).all()
    
    completed = 0
    not_completed = 0
    
    # 统计完成和未完成的数量
    for student in students:
        try:
            # 基础必需项目（男女都需要测试的项目）
            base_items = [
                student.sHeight,
                student.sWeight,
                student.sVitalCapacity,
                student.run50,
                student.standingLongJump,
                student.sittingForward
            ]
            
            # 判断性别特定项目
            if student.sSex == '男':
                # 男生特有项目
                required_items = base_items + [
                    student.run1000,
                    student.pullUP
                ]
            else:
                # 女生特有项目
                required_items = base_items + [
                    student.run800,
                    student.oneMinuteSitUps
                ]
            
            # 检查所有必需项目是否都有数据
            is_completed = all(
                item is not None and 
                str(item).strip() != '' and 
                str(item).lower() != 'none'
                for item in required_items
            )
            
            if is_completed:
                completed += 1
            else:
                not_completed += 1
                
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error processing student {student.sNumber if hasattr(student, 'sNumber') else 'Unknown'}: {str(e)}")
            not_completed += 1
    
    return jsonify({
        'completed': completed,
        'notCompleted': not_completed
    })




# main body
# 各院系在校生参测率
@bp.get('/college_participation_rate')
@login_required
def college_participation_rate():
    # 获取所有学生数据
    students = db.session.query(Student).all()
    
    # 初始化各学院统计数据
    college_stats = {}
    
    # 遍历所有学生
    for student in students:
        try:
            college_code = student.collegeCode
            
            # 如果学院代码不在统计数据中，则初始化该学院的统计数据
            if college_code not in college_stats:
                college_stats[college_code] = {
                    'total': 0,      # 总人数
                    'completed': 0    # 完成体测人数
                }
            
            college_stats[college_code]['total'] += 1
            
            # 基础必需项目（男女都需要测试的项目）
            base_items = [
                student.sHeight,
                student.sWeight,
                student.sVitalCapacity,
                student.run50,
                student.standingLongJump,
                student.sittingForward
            ]
            
            # 判断性别特定项目
            if student.sSex == '男':
                # 男生特有项目
                required_items = base_items + [
                    student.run1000,
                    student.pullUP
                ]
            else:
                # 女生特有项目
                required_items = base_items + [
                    student.run800,
                    student.oneMinuteSitUps
                ]
            
            # 检查所有必需项目是否都有数据
            is_completed = all(
                item is not None and 
                str(item).strip() != '' and 
                str(item).lower() != 'none'
                for item in required_items
            )
            
            if is_completed:
                college_stats[college_code]['completed'] += 1
                
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error processing student {student.sNumber if hasattr(student, 'sNumber') else 'Unknown'}: {str(e)}")
            continue
    
    # 查询学院名称
    colleges = db.session.query(College).all()
    college_names = {college.collegeCode: college.className for college in colleges}
    
    # 计算参测率并格式化数据
    result = []
    for code, stats in college_stats.items():
        if stats['total'] > 0:  # 避免除以零
            participation_rate = round(stats['completed'] / stats['total'] * 100, 2)
            result.append({
                'name': college_names.get(code, f'未知学院({code})'),
                'value': participation_rate
            })
    
    # 按参测率降序排序
    result.sort(key=lambda x: x['value'], reverse=False)
    
    return jsonify({
        'data': result
    })




















