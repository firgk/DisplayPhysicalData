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
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
import os
from flask_caching import Cache


bp = Blueprint('api', __name__, url_prefix='/api')

# 初始化缓存
cache = Cache()


@bp.get('/distribution_of_actual_test_scores')
@login_required  # 如果需要用户登录，取消注释
@cache.cached(timeout=900)
def distribution_of_actual_test_scores():

    students = db.session.query(Student).all()

    # 模拟对成绩进行分组统计，这里以 allScore 为例
    score_ranges = {
        "50 分以下": 0,
        "50 - 60 分": 0,
        "60 - 70 分": 0,
        "70 - 80 分": 0,
        "80 分以上": 0
    }

    for student in students:
        try:
            score = float(student.score_allScore)
            if score < 50:
                score_ranges["50 分以下"] += 1
            elif 50 <= score < 60:
                score_ranges["50 - 60 分"] += 1
            elif 60 <= score < 70:
                score_ranges["60 - 70 分"] += 1
            elif 70 <= score < 80:
                score_ranges["70 - 80 分"] += 1
            elif score >= 80:
                score_ranges["80 分以上"] += 1
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
@cache.cached(timeout=900)
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
@cache.cached(timeout=900)
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
            if score >= 75:
                grade_data[grade]['优秀'] += 1
            elif score >= 65 and score < 75:
                grade_data[grade]['良好'] += 1
            elif score >= 60 and score < 70:
                grade_data[grade]['及格'] += 1
            elif score < 60:
                grade_data[grade]['不及格'] += 1

        except (ValueError, TypeError) as e:
            print(f"处理学生 {student.sNumber} 时发生错误: {str(e)}")  # 添加调试信息
    
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
@cache.cached(timeout=900)
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
@cache.cached(timeout=900)
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


@bp.get('/error_statistics')
@login_required
@cache.cached(timeout=900)
def error_statistics():
    # 获取所有学生数据
    students = db.session.query(Student).all()
    
    # 初始化异常统计
    error_stats = {
        'height': 0,          # 身高异常
        'weight': 0,          # 体重异常
        'vital_capacity': 0,  # 肺活量异常
        'run50': 0,          # 50米跑异常
        'long_jump': 0,      # 立定跳远异常
        'sit_forward': 0,    # 坐位体前屈异常
        'run1000': 0,        # 1000米跑异常
        'pull_up': 0,        # 引体向上异常
        'run800': 0,         # 800米跑异常
        'sit_ups': 0         # 一分钟仰卧起坐异常
    }
    
    # 遍历所有学生
    for student in students:
        try:
            # 检查每个项目的异常情况
            if student.score_error == '1' and student.score_errormessage:
                error_message = student.score_errormessage
                
                # 统计各项异常
                if '身高异常' in error_message:
                    error_stats['height'] += 1
                if '体重异常' in error_message:
                    error_stats['weight'] += 1
                if '肺活量异常' in error_message:
                    error_stats['vital_capacity'] += 1
                if '50米跑异常' in error_message:
                    error_stats['run50'] += 1
                if '立定跳远异常' in error_message:
                    error_stats['long_jump'] += 1
                if '坐位体前屈异常' in error_message:
                    error_stats['sit_forward'] += 1
                if '1000米跑异常' in error_message:
                    error_stats['run1000'] += 1
                if '引体向上异常' in error_message:
                    error_stats['pull_up'] += 1
                if '800米跑异常' in error_message:
                    error_stats['run800'] += 1
                if '一分钟仰卧起坐异常' in error_message:
                    error_stats['sit_ups'] += 1
                    
        except (ValueError, TypeError, AttributeError):
            continue
    
    # 格式化数据为前端需要的格式
    result = [
        {'name': '身高异常', 'value': error_stats['height']},
        {'name': '体重异常', 'value': error_stats['weight']},
        {'name': '肺活量异常', 'value': error_stats['vital_capacity']},
        {'name': '50米跑异常', 'value': error_stats['run50']},
        {'name': '立定跳远异常', 'value': error_stats['long_jump']},
        {'name': '坐位体前屈异常', 'value': error_stats['sit_forward']},
        {'name': '1000米跑异常', 'value': error_stats['run1000']},
        {'name': '引体向上异常', 'value': error_stats['pull_up']},
        {'name': '800米跑异常', 'value': error_stats['run800']},
        {'name': '一分钟仰卧起坐异常', 'value': error_stats['sit_ups']}
    ]
    
    # 按异常数量降序排序
    result.sort(key=lambda x: x['value'], reverse=True)
    return jsonify({
        'data': result[:7]  # 只返回前6条数据
    })



@bp.get('/cluster_analysis_result')
@login_required
@cache.cached(timeout=900)
def cluster_analysis_result():
    try:
        # 读取聚类结果文件
        with open('makedata/student_clusters.json', 'r', encoding='utf-8') as f:
            cluster_data = json.load(f)
            
        # 提取每个群体的特征数据
        clusters = cluster_data['clusters']
        cluster_features = []
        
        for cluster in clusters:
            features = cluster['簇特征']
            cluster_features.append({
                'cluster_id': cluster['簇ID'],
                'student_count': cluster['学生数量'],
                'features': {
                    '身高': features['平均身高'],
                    '体重': features['平均体重'],
                    '肺活量': features['平均肺活量'],
                    '50米跑': features['50米跑平均成绩'],
                    '立定跳远': features['立定跳远平均成绩'],
                    '坐位体前屈': features['坐位体前屈平均成绩'],
                    '长跑': features['长跑平均成绩'],
                    '力量项目': features['力量项目平均成绩']
                }
            })
            
        return jsonify({
            'success': True,
            'data': cluster_features
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': f'获取聚类分析结果失败: {str(e)}'
        })




# 单日体测个数数据统计

@bp.get('/single_day_test_count_data_statistics')
@login_required
@cache.cached(timeout=900)
def single_day_test_count_data_statistics():
    try:
        # 获取所有学生数据
        students = db.session.query(Student).all()
        print(f"获取到的学生总数: {len(students)}")  # 调试信息
        
        # 初始化日期统计字典
        date_stats = {}
        
        # 遍历所有学生
        for student in students:
            try:
                # 获取学生的体测日期
                test_date = student.update_at
                
                if test_date:
                    # 如果日期是字符串，直接使用
                    if isinstance(test_date, str):
                        date_str = test_date.split()[0]  # 只取日期部分，去掉时间
                    else:
                        # 如果是日期对象，转换为字符串
                        date_str = test_date.strftime('%Y-%m-%d')

                    
                    # 统计该日期的体测人数
                    if date_str in date_stats:
                        date_stats[date_str] += 1
                    else:
                        date_stats[date_str] = 1
                else:
                    print(f"学生 {student.sNumber} 没有体测日期")  # 调试信息
                    
            except (ValueError, TypeError, AttributeError) as e:
                print(f"处理学生 {student.sNumber} 时发生错误: {str(e)}")  # 调试信息
                continue
        
        
        # 按日期排序
        sorted_dates = sorted(date_stats.keys())
        
        # 准备返回数据
        result = {
            'dates': sorted_dates,
            'counts': [date_stats[date] for date in sorted_dates]
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        print(f"发生错误: {str(e)}")  # 调试信息
        return jsonify({
            'success': False,
            'msg': f'获取数据失败: {str(e)}'
        })






