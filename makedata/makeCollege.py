# 定义 College 类
class College:
    def __init__(self,collegeCode, className):
        self.collegeCode = collegeCode
        self.className = className

# from applications.models.college import College

college_data = {
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

colleges = []
for className, collegeCode in college_data.items():
    colleges.append(
        College(
            collegeCode=collegeCode,
            className=className
        )
    )


# 打印 studentdata 进行验证
# for student in collegedata:
#     print(f"学院代码: {student.collegeCode}, 学院名称: {student.className}")



output = "colleges = ["
for student in colleges:
    output += f"""
    College(
        collegeCode='{student.collegeCode}',
        className='{student.className}',
    ),"""
output = output.rstrip(',') + "\n]"

# print(output)


with open('../applications/common/script/college.py', 'w', encoding='utf-8') as file:
    file.write('from applications.models import College\n')
    file.write('\n')
    file.write(output)

