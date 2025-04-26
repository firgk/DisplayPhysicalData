from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc
import json
import os
from datetime import datetime

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
    student.collegeCode = college_info.className
    
    # 读取聚类数据
    cluster_data = {}
    try:
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                    'makedata', 'student_clusters.json')
        with open(json_file_path, 'r', encoding='utf-8') as f:
            cluster_data = json.load(f)
        print(cluster_data)
        print('数据加载成功')

    except Exception as e:
        print(f"Error reading cluster data: {e}")
    
    # 获取当前学生的聚类信息
    student_cluster = {}
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
    
    print(student_cluster)
    return render_template('front/index.html', 
                         user=student, 
                         cluster_info=student_cluster)







@bp.get('/cluster-analysis')
@login_required
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







