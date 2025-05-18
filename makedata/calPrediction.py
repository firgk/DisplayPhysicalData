import os
import json
# 预测分析
def unreach_analysis(students, unreach):
    try:

        # 获取所有学生及其补测数据
        unreach_students = []
        
        # 收集需要补测的学生及其数据
        for student in students:
            for unreach_item in unreach:  # 遍历 unreach
                if student.unreach == '1' and unreach_item.student_id == student.id:
                    unreach_students.append((student, unreach_item))
        

        # 分析数据并生成预测
        prediction_results = perform_time_series_analysis(unreach_students)
        regression_results = perform_regression_analysis(unreach_students)
        

        # 将结果保存为JSON文件
        analysis_results = {
            "success": True,
            "msg": "成绩预测分析完成",
            "时间序列分析": prediction_results,
            "回归分析": regression_results,
            "总体评估": generate_overall_assessment(prediction_results)
        }

        
        # Corrected file path construction
        json_file_path = os.path.join(os.path.dirname(__file__),  'unreach_analysis.json')


        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=4)


    except Exception as e:
        print(f"系统运行异常: {str(e)}")
        print("分析失败")
        return 





# 预测分析附加函数
# 时间序列分析

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
            if (feature == 'run1000' and student.sSex == '男') or \
               (feature == 'run800' and student.sSex == '女') or \
               (feature == 'pullUP' and student.sSex == '男') or \
               (feature == 'oneMinuteSitUps' and student.sSex == '女'):
                continue
            
            # 获取第一次和第二次的成绩
            first_score = getattr(student, feature, None)
            second_score = getattr(unreach_student, feature, None)
            
            # 如果有效的成绩数据，计算预测值
            if first_score not in [None, '', 'None'] and second_score not in [None, '', 'None']:
            # if first_score and second_score and first_score != 'None' and second_score != 'None':
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




# 预测分析附加函数
# 回归分析

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




# 预测分析附加函数
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


# 预测分析附加函数

# 总体评估函数

def generate_overall_assessment(time_series_results):
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


# 预测分析附加函数

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



































