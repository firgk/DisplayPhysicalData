

依托
Pear Admin Flask
还未完成



```
init_login


from flask_login import LoginManager


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = 'system.passport.login'

    @login_manager.user_loader
    def load_user(user_id):
        from applications.models import User, Student
        # 首先尝试从User表中查找
        user = User.query.get(int(user_id))
        if user:
            return user
        # 如果User表中没有找到，尝试从Student表中查找
        student = Student.query.get(int(user_id))
        return student
```