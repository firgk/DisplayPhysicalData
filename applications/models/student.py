from datetime import datetime
from applications.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='学生记录ID')
    collegeCode = db.Column(db.String(255), comment='学院编号')
    grade = db.Column(db.String(255), comment='年级')
    classNum = db.Column(db.String(255), comment='班级')
    sNumber = db.Column(db.String(255), nullable=False, comment='学号')
    sName = db.Column(db.String(255), comment='姓名')
    sSex = db.Column(db.String(255), comment='性别')
    sBirthDate = db.Column(db.String(255), comment='出生日期')
    sHeight = db.Column(db.String(255), comment='身高')
    sWeight = db.Column(db.String(255), comment='体重')
    sVitalCapacity = db.Column(db.String(255), comment='肺活量')
    run50 = db.Column(db.String(255), comment='50米跑')
    standingLongJump = db.Column(db.String(255), comment='立定跳远')
    sittingForward = db.Column(db.String(255), comment='坐位体前屈')
    run800 = db.Column(db.String(255), comment='800米跑')
    run1000 = db.Column(db.String(255), comment='1000米跑')
    oneMinuteSitUps = db.Column(db.String(255), comment='一分钟仰卧起坐')
    pullUP = db.Column(db.String(255), comment='引体向上')
    update_at = db.Column(db.String(255), comment='更新时间')

    score_bmi = db.Column(db.String(255), comment='成绩-bmi')  # 15% 体重指数（BMI）=体重（千克）/身高^2（米^2）。
    score_sVitalCapacity = db.Column(db.String(255), comment='成绩-肺活量')  # 15%
    score_run50 = db.Column(db.String(255), comment='成绩-50米跑')  # 20%
    score_standingLongJump = db.Column(db.String(255), comment='成绩-立定跳远')  # 10%
    score_sittingForward = db.Column(db.String(255), comment='成绩-坐位体前屈')  # 10%
    score_run800 = db.Column(db.String(255), comment='成绩-800米跑')  # 20%
    score_run1000 = db.Column(db.String(255), comment='成绩-1000米跑')
    score_oneMinuteSitUps = db.Column(db.String(255), comment='成绩-一分钟仰卧起坐')  # 10%
    score_pullUP = db.Column(db.String(255), comment='成绩-引体向上')
    score_allScore = db.Column(db.String(255), comment='成绩-总成绩')

    score_error = db.Column(db.String(255), comment='是否异常') # 0 正常 1 错误
    score_errormessage = db.Column(db.String(255), comment='异常信息')

    password_hash = db.Column(db.String(128), comment='哈希密码')
    enable = db.Column(db.Integer, default=0, comment='启用')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)






    # def __init__(self, id, collegeCode, grade, classNum, sNumber, sName, sSex, sBirthDate, sHeight, sWeight,
    #              sVitalCapacity,
    #              run50, standingLongJump, sittingForward, run800, run1000, oneMinuteSitUps, pullUP, score_bmi,
    #              score_sVitalCapacity,
    #              score_run50, score_standingLongJump, score_sittingForward, score_run800, score_run1000
    #              , score_oneMinuteSitUps, score_pullUP, score_allScore,
    #                 score_error ,score_errormessage,password_hash,enable
    #              ):
    #     self.id = id
    #     self.collegeCode = collegeCode
    #     self.grade = grade
    #     self.classNum = classNum
    #     self.sNumber = sNumber
    #     self.sName = sName
    #     self.sSex = sSex
    #     self.sBirthDate = sBirthDate
    #     self.sHeight = sHeight
    #     self.sWeight = sWeight
    #     self.sVitalCapacity = sVitalCapacity
    #     self.run50 = run50
    #     self.standingLongJump = standingLongJump
    #     self.sittingForward = sittingForward
    #     self.run800 = run800
    #     self.run1000 = run1000
    #     self.oneMinuteSitUps = oneMinuteSitUps
    #     self.pullUP = pullUP
    #
    #     self.score_bmi = score_bmi
    #     self.score_sVitalCapacity = score_sVitalCapacity
    #     self.score_run50 = score_run50
    #     self.score_standingLongJump = score_standingLongJump
    #     self.score_sittingForward = score_sittingForward
    #     self.score_run800 = score_run800
    #     self.score_run1000 = score_run1000
    #     self.score_oneMinuteSitUps = score_oneMinuteSitUps
    #     self.score_pullUP = score_pullUP
    #     self.score_allScore = score_allScore
    #
    #     self.score_error = score_error
    #     self.score_errormessage = score_errormessage
    #     self.password_hash = password_hash
    #     self.enable = enable


    def __repr__(self):
        return f'<Student {self.id}>'


