from applications.extensions import db

class Unreach(db.Model):
    __tablename__ = 'unreach'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    student_id = db.Column(db.Integer, comment='学生记录ID')
    grade = db.Column(db.String(255), comment='年级')
    sSex = db.Column(db.String(255), comment='性别')
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


    def __repr__(self):
        return f'<Unreach {self.id}>'


