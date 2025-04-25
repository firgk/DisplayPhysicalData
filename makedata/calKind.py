import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import json


# KMeans 算法
def student_cluster_analysis(students, output_file="student_clusters.json"):
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
        print("没有足够的有效数据进行分析")
        return {
            "success": False,
            "msg": "没有足够的有效数据进行分析"
        }
    
    # 数据标准化
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # K-means聚类
    n_clusters = 4  # 将学生分为4个群体
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    # 分析每个簇的特征
    cluster_results = []
    for cluster_id in range(n_clusters):
        cluster_students = [s for i, s in enumerate(valid_students) if clusters[i] == cluster_id]
        
        if not cluster_students:
            continue
            
        # 获取簇中学生的学号和姓名
        student_info = [{"学号": s.sNumber, "姓名": s.sName} for s in cluster_students]
        
        # 计算簇的平均值
        cluster_features = np.array([features[i] for i, c in enumerate(clusters) if c == cluster_id])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成分析报告
        analysis = {
            "簇ID": int(cluster_id),
            "学生数量": len(cluster_students),
            "学生列表": student_info,
            "簇特征": {
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
        
        cluster_results.append(analysis)
    
    # 为每个学生生成个性化建议
    student_recommendations = []
    for i, student in enumerate(valid_students):
        student_cluster = clusters[i]
        student_features = features[i]
        
        # 找到该学生所在簇的平均值
        cluster_features = np.array([features[j] for j, c in enumerate(clusters) if c == student_cluster])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成针对性建议
        suggestions = []
        if student_features[2] < cluster_means[2] * 0.9:  # 肺活量
            suggestions.append("肺活量低于群体平均水平，建议通过游泳、跑步等有氧运动来提高心肺功能")
            
        if student_features[3] > cluster_means[3] * 1.1:  # 50米跑
            suggestions.append("短跑成绩有提升空间，建议加强速度训练和爆发力训练")
            
        if student_features[4] < cluster_means[4] * 0.9:  # 立定跳远
            suggestions.append("下肢爆发力有待提高，建议加强深蹲、跳跃等针对性训练")
            
        if student_features[5] < cluster_means[5] * 0.9:  # 坐位体前屈
            suggestions.append("柔韧性需要提高，建议每天进行拉伸训练")
            
        if len(suggestions) == 0:
            suggestions.append("各项指标都处于良好水平，建议保持当前的训练状态")
        
        student_recommendations.append({
            "学号": student.sNumber,
            "姓名": student.sName,
            "所属群体": int(student_cluster),
            "建议": suggestions
        })
    
    # 保存结果为JSON文件
    result = {
        "success": True,
        "msg": "分析完成",
        "total_students": len(valid_students),
        "cluster_count": n_clusters,
        "clusters": cluster_results,
        "student_recommendations": student_recommendations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"分析结果已保存到 {output_file}")
    
    # 直接返回结果字典，而不是使用jsonify
    return result

def student_cluster_analysis2(students, output_file="student_clusters1.json"):
    """
    使用DBSCAN算法对学生进行聚类分析
    """
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
        print("没有足够的有效数据进行分析")
        return {
            "success": False,
            "msg": "没有足够的有效数据进行分析"
        }
    
    # 数据标准化
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # DBSCAN聚类
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    clusters = dbscan.fit_predict(features_scaled)
    
    # 分析每个簇的特征
    cluster_results = []
    unique_clusters = set(clusters)
    
    for cluster_id in unique_clusters:
        if cluster_id == -1:  # 跳过噪声点
            continue
            
        cluster_students = [s for i, s in enumerate(valid_students) if clusters[i] == cluster_id]
        
        if not cluster_students:
            continue
            
        # 获取簇中学生的学号和姓名
        student_info = [{"学号": s.sNumber, "姓名": s.sName} for s in cluster_students]
        
        # 计算簇的平均值
        cluster_features = np.array([features[i] for i, c in enumerate(clusters) if c == cluster_id])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成分析报告
        analysis = {
            "簇ID": int(cluster_id),
            "学生数量": len(cluster_students),
            "学生列表": student_info,
            "簇特征": {
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
        
        cluster_results.append(analysis)
    
    
    # 为每个学生生成个性化建议
    student_recommendations = []
    for i, student in enumerate(valid_students):
        student_cluster = clusters[i]
        if student_cluster == -1:  # 跳过噪声点
            continue
            
        student_features = features[i]
        
        # 找到该学生所在簇的平均值
        cluster_features = np.array([features[j] for j, c in enumerate(clusters) if c == student_cluster])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成针对性建议
        suggestions = []
        if student_features[2] < cluster_means[2] * 0.9:  # 肺活量
            suggestions.append("肺活量低于群体平均水平，建议通过游泳、跑步等有氧运动来提高心肺功能")
            
        if student_features[3] > cluster_means[3] * 1.1:  # 50米跑
            suggestions.append("短跑成绩有提升空间，建议加强速度训练和爆发力训练")
            
        if student_features[4] < cluster_means[4] * 0.9:  # 立定跳远
            suggestions.append("下肢爆发力有待提高，建议加强深蹲、跳跃等针对性训练")
            
        if student_features[5] < cluster_means[5] * 0.9:  # 坐位体前屈
            suggestions.append("柔韧性需要提高，建议每天进行拉伸训练")
            
        if len(suggestions) == 0:
            suggestions.append("各项指标都处于良好水平，建议保持当前的训练状态")
        
        student_recommendations.append({
            "学号": student.sNumber,
            "姓名": student.sName,
            "所属群体": int(student_cluster),
            "建议": suggestions
        })
    
    # 保存结果为JSON文件
    result = {
        "success": True,
        "msg": "分析完成",
        "total_students": len(valid_students),
        "cluster_count": len(unique_clusters) - 1,  # 减去噪声点
        "clusters": cluster_results,
        "student_recommendations": student_recommendations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"分析结果已保存到 {output_file}")
    return result




def student_cluster_analysis3(students, output_file="student_clusters2.json"):
    """
    使用层次聚类算法对学生进行聚类分析
    """
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
        print("没有足够的有效数据进行分析")
        return {
            "success": False,
            "msg": "没有足够的有效数据进行分析"
        }
    
    # 数据标准化
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # 层次聚类
    n_clusters = 4  # 将学生分为4个群体
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    clusters = hierarchical.fit_predict(features_scaled)
    
    # 分析每个簇的特征
    cluster_results = []
    for cluster_id in range(n_clusters):
        cluster_students = [s for i, s in enumerate(valid_students) if clusters[i] == cluster_id]
        
        if not cluster_students:
            continue
            
        # 获取簇中学生的学号和姓名
        student_info = [{"学号": s.sNumber, "姓名": s.sName} for s in cluster_students]
        
        # 计算簇的平均值
        cluster_features = np.array([features[i] for i, c in enumerate(clusters) if c == cluster_id])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成分析报告
        analysis = {
            "簇ID": int(cluster_id),
            "学生数量": len(cluster_students),
            "学生列表": student_info,
            "簇特征": {
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
        
        cluster_results.append(analysis)
    
    # 为每个学生生成个性化建议
    student_recommendations = []
    for i, student in enumerate(valid_students):
        student_cluster = clusters[i]
        student_features = features[i]
        
        # 找到该学生所在簇的平均值
        cluster_features = np.array([features[j] for j, c in enumerate(clusters) if c == student_cluster])
        cluster_means = np.mean(cluster_features, axis=0)
        
        # 生成针对性建议
        suggestions = []
        if student_features[2] < cluster_means[2] * 0.9:  # 肺活量
            suggestions.append("肺活量低于群体平均水平，建议通过游泳、跑步等有氧运动来提高心肺功能")
            
        if student_features[3] > cluster_means[3] * 1.1:  # 50米跑
            suggestions.append("短跑成绩有提升空间，建议加强速度训练和爆发力训练")
            
        if student_features[4] < cluster_means[4] * 0.9:  # 立定跳远
            suggestions.append("下肢爆发力有待提高，建议加强深蹲、跳跃等针对性训练")
            
        if student_features[5] < cluster_means[5] * 0.9:  # 坐位体前屈
            suggestions.append("柔韧性需要提高，建议每天进行拉伸训练")
            
        if len(suggestions) == 0:
            suggestions.append("各项指标都处于良好水平，建议保持当前的训练状态")
        
        student_recommendations.append({
            "学号": student.sNumber,
            "姓名": student.sName,
            "所属群体": int(student_cluster),
            "建议": suggestions
        })
    
    # 保存结果为JSON文件
    result = {
        "success": True,
        "msg": "分析完成",
        "total_students": len(valid_students),
        "cluster_count": n_clusters,
        "clusters": cluster_results,
        "student_recommendations": student_recommendations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"分析结果已保存到 {output_file}")
    return result
        







