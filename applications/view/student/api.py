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


@bp.get('/error_statistics')
@login_required
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





# 使用聚类算法，对学生体测数据进行聚类分析，分析不同群体特征，并给出决策建议
# 传入一个学生的id，返回聚类结果，和决策建议
#

@bp.get('/student_cluster_analysis/<int:student_id>')
@login_required
def student_cluster_analysis(student_id):
    try:
        # 获取所有学生数据
        students = db.session.query(Student).all()
        target_student = db.session.query(Student).filter_by(id=student_id).first()
        
        if not target_student:
            return fail_api(msg="未找到指定学生")
        
        # 准备数据
        features = []
        valid_students = []
        
        for student in students:
            try:
                # 提取特征（身高、体重、肺活量、50米跑、立定跳远、坐位体前屈）
                height = float(student.sHeight)
                weight = float(student.sWeight)
                vital_capacity = float(student.sVitalCapacity)
                run_50 = float(student.run50)
                long_jump = float(student.standingLongJump)
                sit_forward = float(student.sittingForward)
                
                # 根据性别添加特定项目
                if student.sSex == '男':
                    run_long = float(student.run1000)
                    strength = float(student.pullUP)
                else:
                    run_long = float(student.run800)
                    strength = float(student.oneMinuteSitUps)
                
                features.append([
                    height, weight, vital_capacity, 
                    run_50, long_jump, sit_forward,
                    run_long, strength
                ])
                valid_students.append(student)
                
            except (ValueError, TypeError, AttributeError):
                continue
        
        if not features:
            return fail_api(msg="没有足够的有效数据进行分析")
        
        # 数据标准化
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # K-means聚类
        n_clusters = 4  # 将学生分为4个群体
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        # 找到目标学生所属的簇
        target_index = valid_students.index(target_student)
        target_cluster = clusters[target_index]
        
        # 分析目标学生所在簇的特征
        cluster_students = [s for i, s in enumerate(valid_students) if clusters[i] == target_cluster]
        
        # 计算簇的平均值
        cluster_features = np.array([features[i] for i, c in enumerate(clusters) if c == target_cluster])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成分析报告
        analysis = {
            "cluster_size": len(cluster_students),
            "total_students": len(valid_students),
            "cluster_characteristics": {
                "平均身高": round(cluster_means[0], 2),
                "平均体重": round(cluster_means[1], 2),
                "平均肺活量": round(cluster_means[2], 2),
                "50米跑平均成绩": round(cluster_means[3], 2),
                "立定跳远平均成绩": round(cluster_means[4], 2),
                "坐位体前屈平均成绩": round(cluster_means[5], 2),
                "长跑平均成绩": round(cluster_means[6], 2),
                "力量项目平均成绩": round(cluster_means[7], 2)
            }
        }
        
        # 生成建议
        suggestions = []
        student_features = features[target_index]
        
        # 比较学生个人成绩与簇平均值，生成针对性建议
        if student_features[2] < cluster_means[2] * 0.9:  # 肺活量
            suggestions.append("您的肺活量低于群体平均水平，建议通过游泳、跑步等有氧运动来提高心肺功能")
            
        if student_features[3] > cluster_means[3] * 1.1:  # 50米跑
            suggestions.append("您的短跑成绩有提升空间，建议加强速度训练和爆发力训练")
            
        if student_features[4] < cluster_means[4] * 0.9:  # 立定跳远
            suggestions.append("您的下肢爆发力有待提高，建议加强深蹲、跳跃等针对性训练")
            
        if student_features[5] < cluster_means[5] * 0.9:  # 坐位体前屈
            suggestions.append("您的柔韧性需要提高，建议每天进行拉伸训练")
            
        if len(suggestions) == 0:
            suggestions.append("您的各项指标都处于良好水平，建议保持当前的训练状态")
        
        return jsonify({
            "success": True,
            "msg": "分析完成",
            "analysis": analysis,
            "suggestions": suggestions
        })
        
    except Exception as e:
        return fail_api(msg=f"分析过程中发生错误: {str(e)}")


@bp.get('/cluster_analysis_result')
@login_required
def cluster_analysis_result():
    try:
        # 获取JSON文件路径
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters.json')
        
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 根据群体特征确定群体名称
        def determine_cluster_name(features):
            # 获取关键指标
            run_50 = float(features['50米跑平均成绩'])
            long_jump = float(features['立定跳远平均成绩'])
            vital_capacity = float(features['平均肺活量'])
            sit_forward = float(features['坐位体前屈平均成绩'])
            strength = float(features['力量项目平均成绩'])
            height = float(features['平均身高'])
            weight = float(features['平均体重'])
            
            # 计算BMI
            height_m = height / 100  # 转换为米
            bmi = weight / (height_m * height_m)
            
            # 判断各项指标的水平
            # 力量型特征
            is_strong = (strength > 30 and long_jump > 200) or long_jump > 220
            # 速度型特征
            is_fast = run_50 < 8.3
            # 耐力型特征
            has_endurance = vital_capacity > 3000
            # 柔韧性特征
            is_flexible = sit_forward > 15
            # 体能待发展特征
            needs_improvement = run_50 > 8.8 or long_jump < 180 or vital_capacity < 2800
            
            # 根据特征组合确定类型
            if is_strong and is_fast:
                return "速度力量型"
            elif is_strong and has_endurance:
                return "力量耐力型"
            elif is_fast and is_flexible:
                return "速度灵敏型"
            elif has_endurance and is_flexible:
                return "耐力柔韧型"
            elif needs_improvement:
                return "体能发展型"
            else:
                return "综合平衡型"
            
        # 处理数据以适应图表展示
        cluster_stats_dict = {}
        
        # 首先将相同类型的群体数据合并
        for cluster in data['clusters']:
            cluster_name = determine_cluster_name(cluster['簇特征'])
            if cluster_name not in cluster_stats_dict:
                cluster_stats_dict[cluster_name] = {
                    'name': cluster_name,
                    'value': 0,
                    'features': {k: 0 for k in cluster['簇特征'].keys()},
                    'count': 0
                }
            
            # 累加学生数量
            cluster_stats_dict[cluster_name]['value'] += cluster['学生数量']
            # 累加特征值（用于后面计算平均值）
            for k, v in cluster['簇特征'].items():
                cluster_stats_dict[cluster_name]['features'][k] += float(v) * cluster['学生数量']
            cluster_stats_dict[cluster_name]['count'] += cluster['学生数量']
        
        # 计算合并后的平均特征值
        for cluster_info in cluster_stats_dict.values():
            for k in cluster_info['features'].keys():
                cluster_info['features'][k] = round(
                    cluster_info['features'][k] / cluster_info['count'], 
                    2 if k in ['平均身高', '平均体重'] else 1
                )
            del cluster_info['count']  # 删除临时计数字段
        
        # 转换为列表并排序（按学生数量降序）
        cluster_stats = sorted(
            cluster_stats_dict.values(),
            key=lambda x: x['value'],
            reverse=True
        )
            
        return jsonify({
            'success': True,
            'data': {
                'clusterStats': cluster_stats,
                'totalStudents': data['total_students'],
                'clusterCount': len(cluster_stats),
                'clusters': cluster_stats,
                'recommendations': data['student_recommendations']
            }
        })
        
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'msg': '聚类分析数据文件不存在，请先运行聚类分析'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': f'读取聚类分析数据失败: {str(e)}'
        })




@bp.get('/student_predictions')
@login_required
def student_predictions():
    try:
        # 获取JSON文件路径
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_predictions.json')
        
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'success': True,
            'data': {
                'totalStudents': data['总学生数'],
                'modelScore': data['模型得分'],
                'featureImportance': data['特征重要性']
            }
        })
        
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'msg': '学生预测数据文件不存在，请先运行预测分析'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'msg': f'读取学生预测数据失败: {str(e)}'
        })
    




