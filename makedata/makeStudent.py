import random
import string
from datetime import datetime
from faker import Faker
from calScore import calculate_score
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



class Student():
    def __init__(self, id,collegeCode, grade,classNum, sNumber, sName, sSex, sBirthDate, sHeight, sWeight, sVitalCapacity,run50, standingLongJump, sittingForward, run800, run1000, oneMinuteSitUps, pullUP


                 ):
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
        value = round(random.gauss(mean, std_dev), 2)
        if value > 0:
            return value


# 生成学生数据
def generate_data(num):
    datas = []
    for i in range(num):
        i=i+1
        id=i
        college_name = random.choice(list(colleges.keys()))
        college_code = colleges[college_name]
        grade = f'{random.randint(1, 4)}'
        class_num = f'{random.randint(1, 6)}'
        s_number = ''.join(random.choices(string.digits, k=10))
        s_name = fake.name()
        s_sex = '男' if random.random() < 0.6 else '女'
        s_birth_date = fake.date_of_birth(minimum_age=18, maximum_age=25).strftime('%Y-%m-%d')
        # 根据性别设置身高体重肺活量等数据的均值和标准差
        if s_sex == '男':
            s_height = generate_normal_data(176.1, 5)
            s_weight = generate_normal_data(65.1, 5)
            s_vital_capacity = int(generate_normal_data(2930, 150))
            run50 = generate_normal_data(8.3, 0.5)
            standing_long_jump = generate_normal_data(200, 0.3)
            sitting_forward = generate_normal_data(13.6, 2)
            run1000 = generate_normal_data(228, 0.3)
            pull_up = int(generate_normal_data(7.1, 5))
        else:
            s_height = generate_normal_data(165.9, 5)
            s_weight = generate_normal_data(58.6, 5)
            s_vital_capacity = int(generate_normal_data(2930, 150))
            run50 = generate_normal_data(8.5, 0.5)
            standing_long_jump = generate_normal_data(180, 0.1)
            sitting_forward = generate_normal_data(14.7, 2)
            run800 = generate_normal_data(204, 0.3)
            one_minute_sit_ups = int(generate_normal_data(37.6, 5))

        student = Student(
            id=id,
            collegeCode=college_code,
            grade=grade,
            classNum=class_num,
            sNumber=s_number,
            sName=s_name,
            sSex=s_sex,
            sBirthDate=s_birth_date,
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
num = 11
datas = generate_data(num)


score_data=[]
for student in datas:
    score = calculate_score(student)
    score_data.append(score)


# 格式化输出数据
output = "datas = ["
for data in score_data:
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
        
        score_error='0',
        score_errormessage='',
        password_hash='pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85',
        enable='1'
    ),"""
output = output.rstrip(',') + "\n]"

print(output)

with open('../applications/common/script/student.py', 'w', encoding='utf-8') as file:
    file.write('from applications.models import Student\n')
    file.write('import datetime\n')
    file.write('now_time = datetime.datetime.now()\n')
    file.write('\n')
    file.write(output)


