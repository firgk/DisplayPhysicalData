
## 大学生体测分析与可视化系统


大学生体测分析与可视化系统的设计与实现
（1）以山东理工大学为背景蓝本，参考大学生体质健康报告模拟生成全校相当组织结构与人数数量的数据，系统须实现的前后端包括用户管理、数据采集与存储、大屏可视化、成绩分析与评估，报告生成等功能。
（2）须增加的算法方法包括，异常值检测算法分析体侧数据异常值， 聚类算法：对学生体测数据进行聚类分析，分析不同群体特征，并给出决策建议。预测分析，采用时间序列分析预测体侧成绩趋势，采用回归分析预测学生未来成绩。
（3）注意，系统应有不同角色，对数据有不同的访问权限。










依托

Pear Admin Flask


### 使用项目

```
创建虚拟环境 venv
cd venv
激活虚拟环境
...
克隆项目
git clone https://github.com/firgk/DisplayPhysicalData.git
切换目录
cd DisplayPhysicalData
安装依赖
pip install -r requirements.txt


启动项目
flask --app app.py run -h 0.0.0.0 -p 8000 --debug
or
flask --app app.py run -h 0.0.0.0 -p 8000
or
python app.py

登录界面
http://127.0.0.1:8000/



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


## 存在的问题

```
登录 http://127.0.0.1:8000/student/show/ 接口 自动删除100 101 ... 109 的成绩，使展示的数据更加好看

登录 student id 为 前 10 的会报错，原因参考 def init_login_manager(app):
```








## 二次开发需要注意

需要熟练掌握 Pear Admin Flask， 否则无法进行开发

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




