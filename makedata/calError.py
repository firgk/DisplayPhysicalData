import numpy as np

def calculate_z_score(data):
    """
    计算Z-score
    """
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:  # 避免除以零
        return [0] * len(data)
    return [(x - mean) / std for x in data]


def calculate_error(student, students, z_score_threshold=3.0):
    """
    计算体测数据异常值
    使用Z-score方法检测异常值
    
    Args:
        student: 当前学生对象
        students: 所有学生数据列表
        z_score_threshold: Z-score阈值，默认为3.0
    """
    error_messages = []
    
    try:
        # 1. 身高异常检测
        if student.sHeight:
            heights = [float(s.sHeight) for s in students if s.sHeight]
            height = float(student.sHeight)
            z_scores = calculate_z_score(heights)
            student_z_score = (height - np.mean(heights)) / np.std(heights) if np.std(heights) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"身高异常: {height}cm ")
        
        # 2. 体重异常检测
        if student.sWeight:
            weights = [float(s.sWeight) for s in students if s.sWeight]
            weight = float(student.sWeight)
            z_scores = calculate_z_score(weights)
            student_z_score = (weight - np.mean(weights)) / np.std(weights) if np.std(weights) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"体重异常: {weight}kg")
        
        # 3. 肺活量异常检测
        if student.sVitalCapacity:
            vital_capacities = [float(s.sVitalCapacity) for s in students if s.sVitalCapacity and s.sSex == student.sSex]
            vital_capacity = float(student.sVitalCapacity)
            z_scores = calculate_z_score(vital_capacities)
            student_z_score = (vital_capacity - np.mean(vital_capacities)) / np.std(vital_capacities) if np.std(vital_capacities) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"肺活量异常: {vital_capacity}ml")
        
        # 4. 50米跑异常检测
        if student.run50:
            run50s = [float(s.run50) for s in students if s.run50]
            run50 = float(student.run50)
            z_scores = calculate_z_score(run50s)
            student_z_score = (run50 - np.mean(run50s)) / np.std(run50s) if np.std(run50s) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"50米跑异常: {run50}秒")
        
        # 5. 立定跳远异常检测
        if student.standingLongJump:
            jumps = [float(s.standingLongJump) for s in students if s.standingLongJump]
            jump = float(student.standingLongJump)
            z_scores = calculate_z_score(jumps)
            student_z_score = (jump - np.mean(jumps)) / np.std(jumps) if np.std(jumps) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"立定跳远异常: {jump}米")
        
        # 6. 坐位体前屈异常检测
        if student.sittingForward:
            forwards = [float(s.sittingForward) for s in students if s.sittingForward]
            forward = float(student.sittingForward)
            z_scores = calculate_z_score(forwards)
            student_z_score = (forward - np.mean(forwards)) / np.std(forwards) if np.std(forwards) != 0 else 0
            if abs(student_z_score) > z_score_threshold:
                error_messages.append(f"坐位体前屈异常: {forward}cm")
        
        # 7. 男生特有项目异常检测
        if student.sSex == '男':
            # 1000米跑
            if student.run1000:
                run1000s = [float(s.run1000) for s in students if s.run1000 and s.sSex == '男']
                run1000 = float(student.run1000)
                z_scores = calculate_z_score(run1000s)
                student_z_score = (run1000 - np.mean(run1000s)) / np.std(run1000s) if np.std(run1000s) != 0 else 0
                if abs(student_z_score) > z_score_threshold:
                    error_messages.append(f"1000米跑异常: {run1000}秒")
            
            # 引体向上
            if student.pullUP:
                pullups = [float(s.pullUP) for s in students if s.pullUP and s.sSex == '男']
                pullup = float(student.pullUP)
                z_scores = calculate_z_score(pullups)
                student_z_score = (pullup - np.mean(pullups)) / np.std(pullups) if np.std(pullups) != 0 else 0
                if abs(student_z_score) > z_score_threshold:
                    error_messages.append(f"引体向上异常: {pullup}次")
        
        # 8. 女生特有项目异常检测
        else:
            # 800米跑
            if student.run800:
                run800s = [float(s.run800) for s in students if s.run800 and s.sSex == '女']
                run800 = float(student.run800)
                z_scores = calculate_z_score(run800s)
                student_z_score = (run800 - np.mean(run800s)) / np.std(run800s) if np.std(run800s) != 0 else 0
                if abs(student_z_score) > z_score_threshold:
                    error_messages.append(f"800米跑异常: {run800}秒")
            
            # 一分钟仰卧起坐
            if student.oneMinuteSitUps:
                situps = [float(s.oneMinuteSitUps) for s in students if s.oneMinuteSitUps and s.sSex == '女']
                situp = float(student.oneMinuteSitUps)
                z_scores = calculate_z_score(situps)
                student_z_score = (situp - np.mean(situps)) / np.std(situps) if np.std(situps) != 0 else 0
                if abs(student_z_score) > z_score_threshold:
                    error_messages.append(f"一分钟仰卧起坐异常: {situp}次")
        
        # 更新学生对象的异常信息
        if error_messages:
            student.score_error = '1'  # 标记为有异常
            student.score_errormessage = '; '.join(error_messages)  # 用分号分隔多个异常信息
        else:
            student.score_error = '0'  # 标记为无异常
            student.score_errormessage = ''
        
        return student
        
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error processing student {student.sNumber if hasattr(student, 'sNumber') else 'Unknown'}: {str(e)}")
        # 发生错误时，将学生标记为异常
        student.score_error = '1'
        student.score_errormessage = f'数据处理错误: {str(e)}'
        return student




