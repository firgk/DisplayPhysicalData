import random
import string
import uuid
from datetime import datetime
from faker import Faker
from calScore import calculate_score
from calError import calculate_error
from calScore import calculate_score2
from calKind import student_cluster_analysis
from calKind import student_cluster_analysis2
from calKind import student_cluster_analysis3
from calPrediction import predict_student_performance
import pickle




# from applications.models import Student
# TODO 引入不正确
# TODO pear.application.common 引入不正确

# class Student():
#     def __init__(self, id,scoreId,collegeCode, grade,classNum, sNumber, sName, sSex, sBirthDate, sHeight, sWeight, sVitalCapacity,
#                 run50, standingLongJump, sittingForward, run800, run1000, oneMinuteSitUps, pullUP,score_bmi,  score_sVitalCapacity,
#                  score_run50,  score_standingLongJump,  score_sittingForward,  score_run800,  score_run1000
#      ,  score_oneMinuteSitUps,  score_pullUP, score_allScore):
#         self.id = id
#         self.scoreId = scoreId
#         self.collegeCode = collegeCode
#         self.grade = grade
#         self.classNum = classNum
#         self.sNumber = sNumber
#         self.sName = sName
#         self.sSex = sSex
#         self.sBirthDate = sBirthDate
#         self.sHeight = sHeight
#         self.sWeight = sWeight
#         self.sVitalCapacity = sVitalCapacity
#         self.run50 = run50
#         self.standingLongJump = standingLongJump
#         self.sittingForward = sittingForward
#         self.run800 = run800
#         self.run1000 = run1000
#         self.oneMinuteSitUps = oneMinuteSitUps
#         self.pullUP = pullUP
#
#         self.score_bmi = score_bmi
#         self.score_sVitalCapacity = score_sVitalCapacity
#         self.score_run50 = score_run50
#         self.score_standingLongJump = score_standingLongJump
#         self.score_sittingForward = score_sittingForward
#         self.score_run800 = score_run800
#         self.score_run1000 = score_run1000
#         self.score_oneMinuteSitUps = score_oneMinuteSitUps
#         self.score_pullUP = score_pullUP
#         self.score_allScore = score_allScore
#
#     def __repr__(self):
#         return f'<Student {self.id}>'
#


class Unreach():
    def __init__(self, id, student_id, grade, sSex, sHeight, sWeight, sVitalCapacity,run50, standingLongJump, sittingForward, run800, run1000, oneMinuteSitUps,pullUP):
        self.id = id
        self.student_id = student_id
        self.grade = grade
        self.sSex = sSex
        self.sHeight = sHeight
        self.sWeight = sWeight
        self.sVitalCapacity = sVitalCapacity
        self.run50 = run50
        self.standingLongJump = standingLongJump
        self.sittingForward = sittingForward
        self.run800 = run800
        self.run1000 = run1000
        self.oneMinuteSitUps = oneMinuteSitUps
        self.pullUP = pullUP




class Student():
    def __init__(self, id,collegeCode, grade,classNum, sNumber, sName, sSex, sBirthDate, sHeight, sWeight, sVitalCapacity,run50, standingLongJump, sittingForward, run800, run1000, oneMinuteSitUps, update_at,pullUP):
        self.id = id
        self.collegeCode = collegeCode
        self.grade = grade
        self.classNum = classNum
        self.sNumber = sNumber
        self.sName = sName
        self.sSex = sSex
        self.sBirthDate = sBirthDate
        self.sHeight = sHeight
        self.sWeight = sWeight
        self.sVitalCapacity = sVitalCapacity
        self.run50 = run50
        self.standingLongJump = standingLongJump
        self.sittingForward = sittingForward
        self.update_at = update_at
        self.run800 = run800
        self.run1000 = run1000
        self.oneMinuteSitUps = oneMinuteSitUps
        self.pullUP = pullUP

    def __repr__(self):
        return f'<Student {self.id}>'

# 初始化Faker
fake = Faker('zh_CN')


# 学院信息
colleges = {
    '机械工程学院': '001',
    '交通与车辆工程学院': '002',
    '农业工程与食品科学学院': '003',
    '电气与电子工程学院': '004',
    '计算机科学与技术学院': '005',
    '化学化工学院': '006',
    '建筑工程与空间信息学院': '007',
    '资源与环境工程学院': '008',
    '材料科学与工程学院': '009',
    '生命与医药学院': '010',
    '数学与统计学院': '011',
    '物理与光电工程学院': '012',
    '经济学院': '013',
    '管理学院': '014',
    '文学与新闻传播学院': '015',
    '外国语学院': '016',
    '法学院': '017',
    '马克思主义学院': '018',
    '美术学院': '019',
    '音乐学院': '020',
    '体育学院': '021',
    '鲁泰纺织服装学院': '022',
    '创新创业学院': '023',
    '国际教育学院': '024',
    '教师教育学院': '025',
    '信息管理学院': '026'
}



# 生成正态分布数据
def generate_normal_data(mean, std_dev):
    if std_dev == 0:
        return mean
    while True:
        # value = round(random.gauss(mean, std_dev), 2)
        value = round(random.gauss(mean, mean*0.2), 2) # 保留两位小数
        if value > 0:
            return value


# 生成学生数据
def generate_data(num,starter):
    datas = []
    for i in range(num):
        i=i+1
        id=starter
        starter=starter+1
        college_name = random.choice(list(colleges.keys()))
        college_code = colleges[college_name]
        grade = f'{random.randint(1, 4)}'
        class_num = f'{random.randint(1, 6)}'
        s_number = ''.join(random.choices(string.digits, k=10))
        s_name = fake.name()
        s_sex = '男' if random.random() < 0.6 else '女'
        s_birth_date = fake.date_of_birth(minimum_age=18, maximum_age=25).strftime('%Y-%m-%d')
        update_at=fake.date_between(start_date=datetime(2025, 1, 1), end_date=datetime.now()).strftime('%Y-%m-%d')
        # 根据性别设置身高体重肺活量等数据的均值和标准差
        if s_sex == '男':
            s_height = generate_normal_data(176.1, 10)
            s_weight = generate_normal_data(65.1, 10)
            s_vital_capacity = int(generate_normal_data(4800, 150))
            run50 = generate_normal_data(6.3, 10)
            standing_long_jump = generate_normal_data(270, 10)
            sitting_forward = generate_normal_data(16.6, 10)
            run1000 = generate_normal_data(240, 3)  # 平均值240秒，对应72分左右
            pull_up = int(generate_normal_data(14.1, 10))
        else:
            s_height = generate_normal_data(165.9, 10)
            s_weight = generate_normal_data(58.6, 10)
            s_vital_capacity = int(generate_normal_data(3500, 10))
            run50 = generate_normal_data(7.1, 10)
            standing_long_jump = generate_normal_data(220, 10)
            sitting_forward = generate_normal_data(14.7, 10)
            run800 = generate_normal_data(230, 3)  # 平均值230秒，对应78分左右
            one_minute_sit_ups = int(generate_normal_data(72.6, 10))

        student = Student(
            id=id,
            collegeCode=college_code,
            grade=grade,
            classNum=class_num,
            sNumber=s_number,
            sName=s_name,
            sSex=s_sex,
            sBirthDate=s_birth_date,
            update_at=update_at,
            sHeight=str(s_height),
            sWeight=str(s_weight),
            sVitalCapacity=str(s_vital_capacity),
            run50=str(run50),
            standingLongJump=str(standing_long_jump),
            sittingForward=str(sitting_forward),
            run800=str(run800) if s_sex == '女' else None,
            run1000=str(run1000) if s_sex == '男' else None,
            oneMinuteSitUps=str(one_minute_sit_ups) if s_sex == '女' else None,
            pullUP=str(pull_up) if s_sex == '男' else None
        )
        datas.append(student)
    return datas



# 生成1000条数据

# num = 20
# datas = generate_data(num,0)
#
# students=[]
# for student in datas:
#     student = calculate_score(student)
#     student = calculate_error(student,datas)  # 传入所有学生数据
#     students.append(student)








# 生成 30000 条数据

students = []
batch_size = 1000
num_batches = 31
starter = 0
for i in range(num_batches):
    datas = generate_data(batch_size,starter)
    starter+=1000
    for student in datas:
        student = calculate_score(student)
        student = calculate_error(student, datas)  # 传入所有学生数据
        students.append(student)




# 以二进制持久化 score_data 数据
with open('students31.bin', 'wb') as file:
    pickle.dump(students, file)


# 读取 score_data 数据
# with open('students30.bin', 'rb') as file:
#     students = pickle.load(file)

print("\n正在复制聚类分析文件...")
import shutil
# 拷贝文件student_clusters30.json 到 student_clusters.json
# shutil.copy2('student_clusters30.json', 'student_clusters.json')
# shutil.copy2('student_clusters301.json', 'student_clusters1.json')
# shutil.copy2('student_clusters302.json', 'student_clusters2.json')
print("文件复制完成")


print("\n正在聚类分析...")
student_cluster_analysis(students,'student_clusters31.json')
student_cluster_analysis2(students,'student_clusters131.json')
student_cluster_analysis3(students,'student_clusters231.json')
print("聚类分析完成")

import shutil
# 拷贝文件student_clusters30.json 到 student_clusters.json
shutil.copy2('student_clusters31.json', 'student_clusters.json')
shutil.copy2('student_clusters131.json', 'student_clusters1.json')
shutil.copy2('student_clusters231.json', 'student_clusters2.json')




# unreach 表 再次构建数据
unreach_students = []
i=0
for student in students:
    if student.unreach == '1':
        i=i+1
        unreach_student = Unreach(
            id=i,
            student_id=student.id,
            grade=student.grade,
            sSex=student.sSex,
            sHeight=student.sHeight,
            sWeight='',
            sVitalCapacity='',
            run50='',
            standingLongJump='',
            sittingForward='',
            run800='',
            run1000='',
            oneMinuteSitUps='',
            pullUP=''
        )
        
        if student.sSex == '男':
            s_weight = generate_normal_data(65.1, 10)
            s_vital_capacity = int(generate_normal_data(4800, 150))
            run50 = generate_normal_data(6.3, 10)
            standing_long_jump = generate_normal_data(270, 10)
            sitting_forward = generate_normal_data(16.6, 10)
            run1000 = generate_normal_data(240, 3)  # 平均值240秒，对应72分左右
            pull_up = int(generate_normal_data(14.1, 10))
            
            unreach_student.sWeight = str(s_weight)
            unreach_student.sVitalCapacity = str(s_vital_capacity)
            unreach_student.run50 = str(run50)
            unreach_student.standingLongJump = str(standing_long_jump)
            unreach_student.sittingForward = str(sitting_forward)
            unreach_student.run1000 = str(run1000)
            unreach_student.pullUP = str(pull_up)
        else:
            s_weight = generate_normal_data(58.6, 10)
            s_vital_capacity = int(generate_normal_data(3500, 10))
            run50 = generate_normal_data(7.1, 10)
            standing_long_jump = generate_normal_data(220, 10)
            sitting_forward = generate_normal_data(14.7, 10)
            run800 = generate_normal_data(230, 3)  # 平均值230秒，对应78分左右
            one_minute_sit_ups = int(generate_normal_data(72.6, 10))
            
            unreach_student.sWeight = str(s_weight)
            unreach_student.sVitalCapacity = str(s_vital_capacity)
            unreach_student.run50 = str(run50)
            unreach_student.standingLongJump = str(standing_long_jump)
            unreach_student.sittingForward = str(sitting_forward)
            unreach_student.run800 = str(run800)
            unreach_student.oneMinuteSitUps = str(one_minute_sit_ups)
        
        unreach_student = calculate_score2(unreach_student)
        unreach_students.append(unreach_student)
    






unreach_student_output = "unreach_datas = ["
total = len(unreach_students)
for i, data in enumerate(unreach_students, 1):
    if i % 100 == 0:
        print(f"处理进度: {i}/{total} ({i/total*100:.1f}%)")
    unreach_student_output += f"""
    Unreach(
        id='{data.id}',
        student_id='{data.student_id}',
        grade='{data.grade}',
        sSex='{data.sSex}',
        sHeight='{data.sHeight}',
        sWeight='{data.sWeight}',
        sVitalCapacity='{data.sVitalCapacity}',
        run50='{data.run50}',
        standingLongJump='{data.standingLongJump}',
        sittingForward='{data.sittingForward}',
        run800='{data.run800}',
        run1000='{data.run1000}',
        oneMinuteSitUps='{data.oneMinuteSitUps}',
        pullUP='{data.pullUP}',
        score_bmi='{data.score_bmi}',
        score_sVitalCapacity='{data.score_sVitalCapacity}',
        score_run50='{data.score_run50}',
        score_standingLongJump='{data.score_standingLongJump}',
        score_sittingForward='{data.score_sittingForward}',
        score_run800='{data.score_run800}',
        score_run1000='{data.score_run1000}',
        score_oneMinuteSitUps='{data.score_oneMinuteSitUps}',
        score_pullUP='{data.score_pullUP}',
        score_allScore='{data.score_allScore}',
    ),"""
output = unreach_student_output.rstrip(',') + "\n]"

# print(output)

with open('../applications/common/script/unreach.py', 'w', encoding='utf-8') as file:
    file.write('from applications.models.unreach import Unreach\n')
    file.write('\n')
    file.write(output)














print("\n正在格式化输出数据...")
# 格式化输出数据
output = "datas = ["
total = len(students)
for i, data in enumerate(students, 1):
    if i % 100 == 0:
        print(f"处理进度: {i}/{total} ({i/total*100:.1f}%)")
    output += f"""
    Student(
        id='{data.id}',
        collegeCode='{data.collegeCode}',
        grade='{data.grade}',
        classNum='{data.classNum}',
        sNumber='{data.sNumber}',
        sName='{data.sName}',
        sSex='{data.sSex}',
        sBirthDate='{data.sBirthDate}',
        sHeight='{data.sHeight}',
        sWeight='{data.sWeight}',
        sVitalCapacity='{data.sVitalCapacity}',
        run50='{data.run50}',
        standingLongJump='{data.standingLongJump}',
        sittingForward='{data.sittingForward}',
        run800='{data.run800}',
        run1000='{data.run1000}',
        oneMinuteSitUps='{data.oneMinuteSitUps}',
        pullUP='{data.pullUP}',
        update_at='{data.update_at}',
        score_bmi='{data.score_bmi}',
        score_sVitalCapacity='{data.score_sVitalCapacity}',
        score_run50='{data.score_run50}',
        score_standingLongJump='{data.score_standingLongJump}',
        score_sittingForward='{data.score_sittingForward}',
        score_run800='{data.score_run800}',
        score_run1000='{data.score_run1000}',
        score_oneMinuteSitUps='{data.score_oneMinuteSitUps}',
        score_pullUP='{data.score_pullUP}',
        score_allScore='{data.score_allScore}',
        
        unreach='{data.unreach}',
        
        score_error='{data.score_error}',
        score_errormessage='{data.score_errormessage}',
        password_hash='pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85',
        enable='1'
    ),"""
output = output.rstrip(',') + "\n]"

# print(output)

with open('../applications/common/script/student.py', 'w', encoding='utf-8') as file:
    file.write('from applications.models import Student\n')
    file.write('import datetime\n')
    file.write('now_time = datetime.datetime.now()\n')
    file.write('\n')
    file.write(output)






