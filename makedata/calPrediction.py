import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def predict_student_performance(students, output_file="student_predictions.json"):
    """
    预测学生未来成绩
    
    参数:
    students: 学生数据列表，每个学生包含各项成绩数据
    output_file: 结果保存的JSON文件路径
    
    返回:
    包含预测结果的字典
    """
    # 准备数据
    features = []
    targets = []
    valid_students = []
    feature_names = []
    
    # 确定特征列，根据第一个学生确定可用特征
    if students and hasattr(students[0], '__dict__'):
        all_attrs = vars(students[0])
        # 排除不作为特征的属性
        excluded_attrs = ['sName', 'sNumber', 'sSex', 'sClass', 'sCollege', 'sMajor', 
                         'sTotalScore', 'sGrade', 'id']
        numeric_features = []
        
        # 尝试获取数值型特征
        for attr, value in all_attrs.items():
            if attr not in excluded_attrs:
                try:
                    float_val = float(value)
                    numeric_features.append(attr)
                except (ValueError, TypeError):
                    pass
        
        feature_names = numeric_features
    else:
        return {
            "success": False,
            "msg": "学生数据格式不正确"
        }
    
    # 收集有效数据
    for student in students:
        try:
            student_features = []
            for feature in feature_names:
                val = getattr(student, feature, None)
                if val is not None:
                    student_features.append(float(val))
                else:
                    raise ValueError(f"{feature} 数据缺失")
            
            # 使用总成绩作为目标变量，如果可用
            if hasattr(student, 'sTotalScore') and student.sTotalScore:
                target = float(student.sTotalScore)
            else:
                # 使用平均成绩作为目标变量
                target = sum(student_features) / len(student_features)
            
            features.append(student_features)
            targets.append(target)
            valid_students.append(student)
        except (ValueError, TypeError, AttributeError) as e:
            print(f"处理学生 {getattr(student, 'sName', '未知')} 数据时出错: {e}")
            continue
    
    if len(features) < 10:  # 确保有足够的样本进行训练
        return {
            "success": False,
            "msg": "有效数据不足，至少需要10名学生的完整数据"
        }
    
    # 转换为numpy数组
    X = np.array(features)
    y = np.array(targets)
    
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 训练模型（使用随机森林回归器）
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    # 使用交叉验证评估模型
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
    avg_cv_score = cv_scores.mean()
    
    # 预测结果
    predictions = model.predict(X_scaled)
    
    # 计算预测的置信区间
    predictions_std = np.std([tree.predict(X_scaled) for tree in model.estimators_], axis=0)
    confidence_intervals = 1.96 * predictions_std
    
    # 获取特征重要性
    feature_importance = []
    for i, feature in enumerate(feature_names):
        feature_importance.append({
            "特征名称": feature,
            "重要性得分": float(model.feature_importances_[i])
        })
    
    # 按重要性排序
    feature_importance.sort(key=lambda x: x["重要性得分"], reverse=True)
    
    # 生成学生个体预测结果
    student_predictions = []
    for i, student in enumerate(valid_students):
        actual = targets[i]
        predicted = predictions[i]
        confidence = confidence_intervals[i]
        
        # 计算预测偏差，用于生成改进建议
        deviation = actual - predicted
        performance_suggestions = []
        
        # 基于特征重要性生成建议
        top_features = sorted(range(len(model.feature_importances_)), 
                             key=lambda j: model.feature_importances_[j], 
                             reverse=True)[:3]
        
        for idx in top_features:
            feature = feature_names[idx]
            feature_val = X[i][idx]
            feature_avg = X[:, idx].mean()
            
            # 生成针对性建议
            if feature_val < feature_avg:
                performance_suggestions.append(f"提高{feature}可能对整体成绩有积极影响")
            else:
                performance_suggestions.append(f"继续保持{feature}的良好表现")
        
        student_predictions.append({
            "学号": getattr(student, 'sNumber', '未知'),
            "姓名": getattr(student, 'sName', '未知'),
            "实际成绩": float(actual),
            "预测成绩": float(predicted),
            "置信区间": float(confidence),
            "改进建议": performance_suggestions
        })
    
    # 生成预测趋势图（将图像转为base64编码）
    trend_img = generate_prediction_chart(targets, predictions, confidence_intervals)
    
    # 准备结果字典
    result = {
        "success": True,
        "msg": "预测分析完成",
        "总学生数": len(valid_students),
        "模型得分": float(avg_cv_score),
        "特征重要性": feature_importance,
        "学生预测结果": student_predictions,
        "预测趋势图": trend_img
    }
    
    # 保存结果为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"预测结果已保存到 {output_file}")
    
    return result

def generate_prediction_chart(actual, predicted, confidence):
    """
    生成预测趋势图并转换为base64编码
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(actual, predicted, alpha=0.5)
    
    # 添加对角线（理想预测线）
    min_val = min(min(actual), min(predicted))
    max_val = max(max(actual), max(predicted))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
    
    # 设置图表属性
    plt.xlabel('实际成绩')
    plt.ylabel('预测成绩')
    plt.title('学生成绩预测分析')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 保存图表为内存中的图像
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    
    # 转换为base64编码
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64

def predict_physical_trends(students, output_file="physical_trends.json"):
    """
    分析体侧成绩趋势
    
    参数:
    students: 学生数据列表
    output_file: 结果保存的JSON文件路径
    
    返回:
    包含趋势分析的字典
    """
    # 检查是否有体测相关的数据
    physical_features = [
        'sHeight', 'sWeight', 'sVitalCapacity', 'run50', 
        'standingLongJump', 'sittingForward', 'run1000', 
        'run800', 'pullUP', 'oneMinuteSitUps'
    ]
    
    valid_data = {}
    for feature in physical_features:
        valid_data[feature] = []
    
    valid_students = []
    
    # 收集有效数据
    for student in students:
        has_valid_data = False
        for feature in physical_features:
            if hasattr(student, feature):
                try:
                    value = float(getattr(student, feature))
                    valid_data[feature].append((student, value))
                    has_valid_data = True
                except (ValueError, TypeError):
                    pass
        
        if has_valid_data:
            valid_students.append(student)
    
    if not valid_students:
        return {
            "success": False,
            "msg": "没有足够的体测数据进行趋势分析"
        }
    
    # 分析每个体测项目的趋势
    trend_analysis = []
    for feature in physical_features:
        feature_data = valid_data[feature]
        if len(feature_data) < 5:  # 需要足够的数据点
            continue
        
        # 对项目数据进行排序和分析
        sorted_data = sorted(feature_data, key=lambda x: x[1])
        values = [d[1] for d in sorted_data]
        
        # 计算统计指标
        mean_val = np.mean(values)
        median_val = np.median(values)
        std_val = np.std(values)
        
        # 识别表现优秀和需要改进的学生
        top_students = sorted_data[-3:] if len(sorted_data) >= 3 else sorted_data[-1:]
        bottom_students = sorted_data[:3] if len(sorted_data) >= 3 else sorted_data[:1]
        
        # 创建项目分析结果
        feature_analysis = {
            "项目名称": feature,
            "参与人数": len(feature_data),
            "平均值": float(mean_val),
            "中位数": float(median_val),
            "标准差": float(std_val),
            "表现优秀学生": [{"学号": s[0].sNumber, "姓名": s[0].sName, "成绩": float(s[1])} 
                       for s in top_students],
            "需要改进学生": [{"学号": s[0].sNumber, "姓名": s[0].sName, "成绩": float(s[1])} 
                       for s in bottom_students]
        }
        
        trend_analysis.append(feature_analysis)
    
    # 生成总体体测趋势分析
    result = {
        "success": True,
        "msg": "体测成绩趋势分析完成",
        "总学生数": len(valid_students),
        "项目分析": trend_analysis
    }
    
    # 保存结果为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"体测成绩趋势分析已保存到 {output_file}")
    
    return result
