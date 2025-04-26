

依托

Pear Admin Flask


### 使用项目

```
创建虚拟环境 venv
cd venv
git clone git@github.com:firgk/DisplayPhysicalData.git
cd DisplayPhysicalData

启动项目
flask --app app.py run -h 0.0.0.0 -p 8000 --debug
or
flask --app app.py run -h 0.0.0.0 -p 8000
or
python app.py

```




````
密码 123456
账号如下：

admin
dean
input
show



不及格之后补测的

4917031304
6757807427


没有补测的

7003341534
5717270489




```



```


修改权限管理之后重新登陆生效

@bp.get('/show/')
show 后要加 / 否则会报错

循环引用导致出错

view/system/rights.py 可以修改部分设置






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




