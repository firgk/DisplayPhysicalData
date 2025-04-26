from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc
import json
import os
from datetime import datetime
from flask_caching import Cache

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models.unreach import Unreach
from applications.models import User, AdminLog,College,Student

bp = Blueprint('front', __name__, url_prefix='/front')

# 初始化缓存
cache = Cache()

# 此处修改需要和 /system/index 下同步
# 此处不需要更改
@bp.get('/main/')
@login_required
def index():
    student = current_user
    college_info = College.query.filter_by(collegeCode=student.collegeCode).first()
    student.collegeCode = college_info.className
    
    # 读取聚类数据
    cluster_data = {}
    student_cluster = {}
    try:
        json_file_path_cluster = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters.json')
        if os.path.exists(json_file_path_cluster):
            with open(json_file_path_cluster, 'r', encoding='utf-8') as f:
                cluster_data = json.load(f)
            print('聚类数据加载成功')

            # 获取当前学生的聚类信息
            if cluster_data and 'clusters' in cluster_data:
                # 遍历所有聚类
                for cluster in cluster_data['clusters']:
                    # 检查该聚类中是否包含当前学生
                    for student_info in cluster['学生列表']:
                        if student_info['学号'] == str(student.sNumber):
                            # 根据簇特征生成类别描述
                            characteristics = cluster['簇特征']
                            cluster_description = "身体素质"
                            if characteristics['平均身高'] > 180:
                                cluster_description += "较高"
                            elif characteristics['平均身高'] < 160:
                                cluster_description += "较低"
                            else:
                                cluster_description += "中等"
                            
                            if characteristics['平均体重'] > 70:
                                cluster_description += "，体型偏重"
                            elif characteristics['平均体重'] < 55:
                                cluster_description += "，体型偏轻"
                            else:
                                cluster_description += "，体型适中"
                            
                            student_cluster = {
                                'cluster': cluster_description,
                                'description': f'该类别共有{cluster["学生数量"]}名学生',
                                'characteristics': cluster['簇特征'],
                                'suggestions': []
                            }
                            # 查找该学生的建议
                            for recommendation in cluster_data.get('student_recommendations', []):
                                if recommendation['学号'] == str(student.sNumber):
                                    student_cluster['suggestions'] = recommendation['建议']
                                    break
                            break
                    if student_cluster:  # 如果找到了学生信息，就退出循环
                        break
        else:
            print("聚类数据文件不存在")

    except Exception as e:
        print(f"读取聚类数据时出错: {e}")

    # 如果学生需要补测，则加载预测分析数据
    prediction_data = None
    if student.unreach == '1':
        try:
            json_file_path_unreach = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                              'makedata', 'unreach_analysis.json')
            if os.path.exists(json_file_path_unreach):
                with open(json_file_path_unreach, 'r', encoding='utf-8') as f:
                    analysis_results = json.load(f)
                print('预测分析数据加载成功')

                # 查找当前学生的预测数据
                student_sNumber_str = str(student.sNumber)
                time_series_result = next((item for item in analysis_results.get("时间序列分析", []) if item.get("学号") == student_sNumber_str), None)
                regression_result = next((item for item in analysis_results.get("回归分析", []) if item.get("学号") == student_sNumber_str), None)

                if time_series_result or regression_result:
                     prediction_data = {
                         "time_series": time_series_result,
                         "regression": regression_result
                     }
                     print(f"找到学生 {student_sNumber_str} 的预测数据")
                else:
                     print(f"未找到学生 {student_sNumber_str} 的预测数据")

            else:
                print("预测分析数据文件不存在")

        except Exception as e:
            print(f"读取预测分析数据时出错: {e}")
    
    print("传递给模板的聚类信息:", student_cluster)
    print("传递给模板的预测信息:", prediction_data)

    return render_template('front/index.html', 
                         user=student, 
                         cluster_info=student_cluster,
                         prediction_info=prediction_data) # 传递预测数据







@bp.get('/cluster-analysis')
@login_required
@cache.cached(timeout=900)
def cluster_analysis():
    try:
        # 读取聚类数据
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cluster_data = json.load(f)
        
        # 处理所有聚类数据
        processed_clusters = []
        if cluster_data and 'clusters' in cluster_data:
            for cluster in cluster_data['clusters']:
                # 根据簇特征生成类别描述
                characteristics = cluster['簇特征']
                cluster_description = "身体素质"
                if characteristics['平均身高'] > 180:
                    cluster_description += "较高"
                elif characteristics['平均身高'] < 160:
                    cluster_description += "较低"
                else:
                    cluster_description += "中等"
                
                if characteristics['平均体重'] > 70:
                    cluster_description += "，体型偏重"
                elif characteristics['平均体重'] < 55:
                    cluster_description += "，体型偏轻"
                else:
                    cluster_description += "，体型适中"
                
                processed_cluster = {
                    'cluster_id': cluster['簇ID'],
                    'cluster_description': cluster_description,
                    'student_count': cluster['学生数量'],
                    'characteristics': {
                        '平均身高': round(characteristics['平均身高'], 2),
                        '平均体重': round(characteristics['平均体重'], 2),
                        '平均肺活量': round(characteristics['平均肺活量'], 2),
                        '50米跑平均成绩': round(characteristics['50米跑平均成绩'], 2),
                        '立定跳远平均成绩': round(characteristics['立定跳远平均成绩'], 2),
                        '坐位体前屈平均成绩': round(characteristics['坐位体前屈平均成绩'], 2),
                        '长跑平均成绩': round(characteristics['长跑平均成绩'], 2),
                        '力量项目平均成绩': round(characteristics['力量项目平均成绩'], 2)
                    }
                }
                processed_clusters.append(processed_cluster)
        
        # 获取所有学生的建议
        all_recommendations = []
        if 'student_recommendations' in cluster_data:
            # 按群体分组建议
            group_recommendations = {}
            for rec in cluster_data['student_recommendations']:
                group_id = rec['所属群体']
                # 找到对应的群体描述
                group_description = None
                for cluster in processed_clusters:
                    if cluster['cluster_id'] == group_id:
                        group_description = cluster['cluster_description']
                        break
                
                if group_description not in group_recommendations:
                    group_recommendations[group_description] = set()
                group_recommendations[group_description].update(rec['建议'])
            
            # 转换为列表格式
            for group_description, suggestions in group_recommendations.items():
                all_recommendations.append({
                    '所属群体': group_description,
                    '建议': list(suggestions)
                })
        
        return table_api(
            msg="获取聚类数据成功",
            data={
                'total_students': cluster_data.get('total_students', 0),
                'cluster_count': cluster_data.get('cluster_count', 0),
                'clusters': processed_clusters,
                'recommendations': all_recommendations
            },
            count=len(processed_clusters)
        )
    except Exception as e:
        return fail_api(msg=f"获取聚类数据失败: {str(e)}")




@bp.get('/cluster-analysis1')
@login_required
@cache.cached(timeout=900)
def cluster_analysis1():
    try:
        # 读取聚类数据
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters1.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cluster_data = json.load(f)
        
        # 处理所有聚类数据
        processed_clusters = []
        if cluster_data and 'clusters' in cluster_data:
            for cluster in cluster_data['clusters']:
                # 根据簇特征生成类别描述
                characteristics = cluster['簇特征']
                cluster_description = "身体素质"
                if characteristics['平均身高'] > 180:
                    cluster_description += "较高"
                elif characteristics['平均身高'] < 160:
                    cluster_description += "较低"
                else:
                    cluster_description += "中等"
                
                if characteristics['平均体重'] > 70:
                    cluster_description += "，体型偏重"
                elif characteristics['平均体重'] < 55:
                    cluster_description += "，体型偏轻"
                else:
                    cluster_description += "，体型适中"
                
                processed_cluster = {
                    'cluster_id': cluster['簇ID'],
                    'cluster_description': cluster_description,
                    'student_count': cluster['学生数量'],
                    'characteristics': {
                        '平均身高': round(characteristics['平均身高'], 2),
                        '平均体重': round(characteristics['平均体重'], 2),
                        '平均肺活量': round(characteristics['平均肺活量'], 2),
                        '50米跑平均成绩': round(characteristics['50米跑平均成绩'], 2),
                        '立定跳远平均成绩': round(characteristics['立定跳远平均成绩'], 2),
                        '坐位体前屈平均成绩': round(characteristics['坐位体前屈平均成绩'], 2),
                        '长跑平均成绩': round(characteristics['长跑平均成绩'], 2),
                        '力量项目平均成绩': round(characteristics['力量项目平均成绩'], 2)
                    }
                }
                processed_clusters.append(processed_cluster)
        
        # 获取所有学生的建议
        all_recommendations = []
        if 'student_recommendations' in cluster_data:
            # 按群体分组建议
            group_recommendations = {}
            for rec in cluster_data['student_recommendations']:
                group_id = rec['所属群体']
                # 找到对应的群体描述
                group_description = None
                for cluster in processed_clusters:
                    if cluster['cluster_id'] == group_id:
                        group_description = cluster['cluster_description']
                        break
                
                if group_description not in group_recommendations:
                    group_recommendations[group_description] = set()
                group_recommendations[group_description].update(rec['建议'])
            
            # 转换为列表格式
            for group_description, suggestions in group_recommendations.items():
                all_recommendations.append({
                    '所属群体': group_description,
                    '建议': list(suggestions)
                })
        
        return table_api(
            msg="获取聚类数据成功",
            data={
                'total_students': cluster_data.get('total_students', 0),
                'cluster_count': cluster_data.get('cluster_count', 0),
                'clusters': processed_clusters,
                'recommendations': all_recommendations
            },
            count=len(processed_clusters)
        )
    except Exception as e:
        return fail_api(msg=f"获取聚类数据失败: {str(e)}")




@bp.get('/cluster-analysis2')
@login_required
@cache.cached(timeout=900)
def cluster_analysis2():
    try:
        # 读取聚类数据
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters2.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cluster_data = json.load(f)
        
        # 处理所有聚类数据
        processed_clusters = []
        if cluster_data and 'clusters' in cluster_data:
            for cluster in cluster_data['clusters']:
                # 根据簇特征生成类别描述
                characteristics = cluster['簇特征']
                cluster_description = "身体素质"
                if characteristics['平均身高'] > 180:
                    cluster_description += "较高"
                elif characteristics['平均身高'] < 160:
                    cluster_description += "较低"
                else:
                    cluster_description += "中等"
                
                if characteristics['平均体重'] > 70:
                    cluster_description += "，体型偏重"
                elif characteristics['平均体重'] < 55:
                    cluster_description += "，体型偏轻"
                else:
                    cluster_description += "，体型适中"
                
                processed_cluster = {
                    'cluster_id': cluster['簇ID'],
                    'cluster_description': cluster_description,
                    'student_count': cluster['学生数量'],
                    'characteristics': {
                        '平均身高': round(characteristics['平均身高'], 2),
                        '平均体重': round(characteristics['平均体重'], 2),
                        '平均肺活量': round(characteristics['平均肺活量'], 2),
                        '50米跑平均成绩': round(characteristics['50米跑平均成绩'], 2),
                        '立定跳远平均成绩': round(characteristics['立定跳远平均成绩'], 2),
                        '坐位体前屈平均成绩': round(characteristics['坐位体前屈平均成绩'], 2),
                        '长跑平均成绩': round(characteristics['长跑平均成绩'], 2),
                        '力量项目平均成绩': round(characteristics['力量项目平均成绩'], 2)
                    }
                }
                processed_clusters.append(processed_cluster)
        
        # 获取所有学生的建议
        all_recommendations = []
        if 'student_recommendations' in cluster_data:
            # 按群体分组建议
            group_recommendations = {}
            for rec in cluster_data['student_recommendations']:
                group_id = rec['所属群体']
                # 找到对应的群体描述
                group_description = None
                for cluster in processed_clusters:
                    if cluster['cluster_id'] == group_id:
                        group_description = cluster['cluster_description']
                        break
                
                if group_description not in group_recommendations:
                    group_recommendations[group_description] = set()
                group_recommendations[group_description].update(rec['建议'])
            
            # 转换为列表格式
            for group_description, suggestions in group_recommendations.items():
                all_recommendations.append({
                    '所属群体': group_description,
                    '建议': list(suggestions)
                })
        
        return table_api(
            msg="获取聚类数据成功",
            data={
                'total_students': cluster_data.get('total_students', 0),
                'cluster_count': cluster_data.get('cluster_count', 0),
                'clusters': processed_clusters,
                'recommendations': all_recommendations
            },
            count=len(processed_clusters)
        )
    except Exception as e:
        return fail_api(msg=f"获取聚类数据失败: {str(e)}")




@bp.get('/unreach-analysis')
@login_required
@cache.cached(timeout=900)
def unreach_analysis():
    try:
        # 获取所有学生及其补测数据
        students = Student.query.all()
        unreach_students = []
        
        # 收集需要补测的学生及其数据
        for student in students:
            if student.unreach == '1':
                unreach_student = Unreach.query.filter_by(student_id=student.id).first()
                if unreach_student:
                    unreach_students.append((student, unreach_student))
        
        if not unreach_students:
            return fail_api(msg="没有找到需要补测的学生数据")
        
        # 分析数据并生成预测
        prediction_results = perform_time_series_analysis(unreach_students)
        regression_results = perform_regression_analysis(unreach_students)
        
        # 将结果保存为JSON文件
        analysis_results = {
            "success": True,
            "msg": "成绩预测分析完成",
            "时间序列分析": prediction_results,
            "回归分析": regression_results,
            "总体评估": generate_overall_assessment(prediction_results, regression_results)
        }
        
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                      'makedata', 'unreach_analysis.json')
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=4)
        
        return table_api(
            msg="成绩预测分析完成",
            data=analysis_results,
            count=len(unreach_students)
        )
    except Exception as e:
        return fail_api(msg=f"成绩预测分析失败: {str(e)}")

def perform_time_series_analysis(unreach_students):
    """
    对学生第一次和第二次体测成绩进行时间序列分析，预测未来成绩趋势
    """
    time_series_results = []
    
    physical_features = [
        'sHeight', 'sWeight', 'sVitalCapacity', 'run50', 
        'standingLongJump', 'sittingForward', 'run800', 'run1000',
        'oneMinuteSitUps', 'pullUP'
    ]
    
    for student, unreach_student in unreach_students:
        student_prediction = {
            "学号": student.sNumber,
            "姓名": student.sName,
            "性别": student.sSex,
            "项目预测": []
        }
        
        for feature in physical_features:
            # 检查该项目是否适用于当前学生性别
            if (feature == 'run800' and student.sSex == '男') or \
               (feature == 'run1000' and student.sSex == '女') or \
               (feature == 'oneMinuteSitUps' and student.sSex == '男') or \
               (feature == 'pullUP' and student.sSex == '女'):
                continue
            
            # 获取第一次和第二次的成绩
            first_score = getattr(student, feature, None)
            second_score = getattr(unreach_student, feature, None)
            
            # 如果有效的成绩数据，计算预测值
            if first_score and second_score and first_score != 'None' and second_score != 'None':
                try:
                    first_value = float(first_score)
                    second_value = float(second_score)
                    
                    # 计算简单线性趋势
                    diff = second_value - first_value
                    trend = "上升" if diff > 0 else "下降" if diff < 0 else "稳定"
                    
                    # 预测第三次成绩 (简单线性外推)
                    predicted_value = second_value + diff
                    
                    # 对某些特定项目进行约束（比如成绩不能为负数）
                    if feature in ['sHeight', 'sWeight', 'sVitalCapacity', 'standingLongJump', 'sittingForward', 'oneMinuteSitUps', 'pullUP']:
                        predicted_value = max(0, predicted_value)
                    
                    # 成绩评级（简单判断）
                    rating = ""
                    if feature in ['sHeight', 'sWeight', 'sVitalCapacity', 'standingLongJump', 'sittingForward', 'oneMinuteSitUps', 'pullUP']:
                        # 这些项目是值越高越好
                        if diff > 0:
                            rating = "继续保持，有进步"
                        else:
                            rating = "需要加强训练"
                    else:
                        # 这些项目是值越低越好（跑步时间）
                        if diff < 0:
                            rating = "继续保持，有进步"
                        else:
                            rating = "需要加强训练"
                    
                    student_prediction["项目预测"].append({
                        "项目名称": feature,
                        "第一次成绩": first_value,
                        "第二次成绩": second_value,
                        "变化趋势": trend,
                        "预测下次成绩": round(predicted_value, 2),
                        "评估": rating
                    })
                except (ValueError, TypeError):
                    pass
        
        # 只有当有预测结果时才添加该学生
        if student_prediction["项目预测"]:
            time_series_results.append(student_prediction)
    
    return time_series_results



def perform_regression_analysis(unreach_students):
    """
    使用回归分析预测学生未来成绩
    """
    regression_results = []
    
    # 按性别分组进行分析
    male_students = [(s, u) for s, u in unreach_students if s.sSex == '男']
    female_students = [(s, u) for s, u in unreach_students if s.sSex == '女']
    
    # 分析男生数据
    if male_students:
        regression_results.extend(analyze_by_gender(male_students, '男'))
    
    # 分析女生数据
    if female_students:
        regression_results.extend(analyze_by_gender(female_students, '女'))
    
    return regression_results

def analyze_by_gender(gender_students, gender):
    """
    针对特定性别的学生进行回归分析
    """
    results = []
    
    # 确定该性别需要分析的项目
    if gender == '男':
        run_project = 'run1000'
        strength_project = 'pullUP'
    else:
        run_project = 'run800'
        strength_project = 'oneMinuteSitUps'
    
    # 基础体能项目（共有的）
    common_projects = ['sHeight', 'sWeight', 'sVitalCapacity', 'run50', 'standingLongJump', 'sittingForward']
    
    for student, unreach_student in gender_students:
        # 收集两次测试的数据
        student_data = {
            "学号": student.sNumber,
            "姓名": student.sName,
            "性别": gender,
            "年级": student.grade,
            "体能评估": [],
            "总体预测": ""
        }
        
        # 分析基础项目
        total_improvement = 0
        valid_projects = 0
        
        for project in common_projects + [run_project, strength_project]:
            first_score = getattr(student, project, None)
            second_score = getattr(unreach_student, project, None)
            
            if first_score and second_score and first_score != 'None' and second_score != 'None':
                try:
                    first_value = float(first_score)
                    second_value = float(second_score)
                    
                    # 计算改进率
                    if project in ['run50', run_project]:  # 跑步项目，时间越短越好
                        improvement = (first_value - second_value) / first_value * 100 if first_value != 0 else 0
                    else:  # 其他项目，值越大越好
                        improvement = (second_value - first_value) / first_value * 100 if first_value != 0 else 0
                    
                    # 预测下一次可能的成绩（基于改进率的简单预测）
                    if project in ['run50', run_project]:
                        predicted = second_value * (1 - improvement/200)  # 减缓改进幅度
                    else:
                        predicted = second_value * (1 + improvement/200)  # 减缓改进幅度
                    
                    # 评估和建议
                    if improvement > 5:
                        assessment = "显著进步，继续保持"
                    elif improvement > 0:
                        assessment = "有所进步，可以更好"
                    elif improvement > -5:
                        assessment = "基本稳定，需加强训练"
                    else:
                        assessment = "有所退步，需重点关注"
                    
                    student_data["体能评估"].append({
                        "项目": project,
                        "首次成绩": first_value,
                        "补测成绩": second_value,
                        "改进率": round(improvement, 2),
                        "预测成绩": round(predicted, 2),
                        "评估": assessment
                    })
                    
                    # 累计总体改进情况
                    total_improvement += improvement
                    valid_projects += 1
                    
                except (ValueError, TypeError):
                    pass
        
        # 生成总体评估
        if valid_projects > 0:
            avg_improvement = total_improvement / valid_projects
            
            if avg_improvement > 10:
                student_data["总体预测"] = "学生整体表现优秀，预计将持续进步并达到优秀水平"
            elif avg_improvement > 5:
                student_data["总体预测"] = "学生有明显进步，有望达到良好水平"
            elif avg_improvement > 0:
                student_data["总体预测"] = "学生有小幅进步，通过努力可达到及格水平"
            else:
                student_data["总体预测"] = "学生需加强训练，重点关注薄弱项目，以达到及格标准"
            
            results.append(student_data)
    
    return results

def generate_overall_assessment(time_series_results, regression_results):
    """
    基于时间序列分析和回归分析生成总体评估报告
    """
    # 统计进步和退步的学生人数
    improving_students = 0
    declining_students = 0
    stable_students = 0
    
    # 从时间序列分析中提取趋势信息
    for student in time_series_results:
        improving_projects = 0
        declining_projects = 0
        
        for project in student["项目预测"]:
            if project["变化趋势"] == "上升" and project["项目名称"] not in ["run50", "run800", "run1000"]:
                improving_projects += 1
            elif project["变化趋势"] == "下降" and project["项目名称"] in ["run50", "run800", "run1000"]:
                improving_projects += 1
            elif project["变化趋势"] == "下降" and project["项目名称"] not in ["run50", "run800", "run1000"]:
                declining_projects += 1
            elif project["变化趋势"] == "上升" and project["项目名称"] in ["run50", "run800", "run1000"]:
                declining_projects += 1
        
        if improving_projects > declining_projects:
            improving_students += 1
        elif improving_projects < declining_projects:
            declining_students += 1
        else:
            stable_students += 1
    
    # 计算各类学生的百分比
    total_students = len(time_series_results)
    if total_students > 0:
        improving_percentage = improving_students / total_students * 100
        declining_percentage = declining_students / total_students * 100
        stable_percentage = stable_students / total_students * 100
    else:
        improving_percentage = declining_percentage = stable_percentage = 0
    
    # 生成总体评估报告
    assessment = {
        "总学生数": total_students,
        "整体趋势": {
            "进步学生数": improving_students,
            "进步学生百分比": round(improving_percentage, 2),
            "稳定学生数": stable_students,
            "稳定学生百分比": round(stable_percentage, 2),
            "退步学生数": declining_students,
            "退步学生百分比": round(declining_percentage, 2)
        },
        "建议措施": []
    }
    
    # 根据数据分析结果生成建议
    if improving_percentage >= 60:
        assessment["建议措施"].append("大多数学生呈现进步趋势，应继续保持现有训练方法")
    elif declining_percentage >= 40:
        assessment["建议措施"].append("较多学生存在退步情况，需要检查训练方法是否合适")
    
    # 添加具体项目的建议
    weak_projects = find_weak_projects(time_series_results)
    for project, count in weak_projects.items():
        if count >= total_students * 0.3:  # 如果30%以上的学生在该项目有问题
            if project == 'sVitalCapacity':
                assessment["建议措施"].append("肺活量普遍较弱，建议增加有氧训练")
            elif project in ['run50', 'run800', 'run1000']:
                assessment["建议措施"].append("跑步项目表现不佳，建议加强耐力和速度训练")
            elif project == 'standingLongJump':
                assessment["建议措施"].append("立定跳远成绩有待提高，建议加强下肢力量训练")
            elif project == 'sittingForward':
                assessment["建议措施"].append("坐位体前屈成绩较差，建议加强柔韧性训练")
            elif project in ['oneMinuteSitUps', 'pullUP']:
                assessment["建议措施"].append("力量项目需要加强，建议增加针对性的力量训练")
    
    return assessment

def find_weak_projects(time_series_results):
    """
    找出学生普遍较弱的项目
    """
    weak_projects = {}
    
    for student in time_series_results:
        for project in student["项目预测"]:
            if (project["变化趋势"] == "下降" and project["项目名称"] not in ["run50", "run800", "run1000"]) or \
               (project["变化趋势"] == "上升" and project["项目名称"] in ["run50", "run800", "run1000"]):
                weak_projects[project["项目名称"]] = weak_projects.get(project["项目名称"], 0) + 1
    
    return weak_projects



































