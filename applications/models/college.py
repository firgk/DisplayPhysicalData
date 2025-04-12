from applications.extensions import db

class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='学院ID')
    collegeCode = db.Column(db.String(255), comment='学院编号')
    className = db.Column(db.String(255), comment='学院名称')

    def __repr__(self):
        return f'<College {self.collegeCode}>'
