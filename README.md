
## 大学生体测分析与可视化系统

```
大学生体测分析与可视化系统的设计与实现
（1）以山东理工大学为背景蓝本，参考大学生体质健康报告模拟生成全校相当组织结构与人数数量的数据，系统须实现的前后端包括用户管理、数据采集与存储、大屏可视化、成绩分析与评估，报告生成等功能。
（2）须增加的算法方法包括，异常值检测算法分析体侧数据异常值， 聚类算法：对学生体测数据进行聚类分析，分析不同群体特征，并给出决策建议。预测分析，采用时间序列分析预测体侧成绩趋势，采用回归分析预测学生未来成绩。
（3）注意，系统应有不同角色，对数据有不同的访问权限。
```









依托

Pear Admin Flask

## 演示视频

https://www.bilibili.com/video/BV1rDLdzSEqS/

### 使用项目

python 3.11.2
linux


python 3.9.20
linux 会报错，需要自己处理 pip

```
创建虚拟环境 test_venv
cd test_venv
激活虚拟环境
...
克隆项目
git clone https://github.com/firgk/display_physical_data.git
切换目录
cd display_physical_data
安装依赖
pip install -r requirements.txt


启动项目
./run



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

9764397200
6092287451


没有补测的

8683340123 曹冬梅
9037491254 王倩


```




## 注意

```
1
登录 http://127.0.0.1:8000/student/show/ 接口 自动删除1001 1002 ... 1009 的成绩，使展示的数据更加好看
启动后首次加载才可以，否则就会由缓存处理，不再执行删除操作

2
def init_login_manager(app):

passport.py 登录


3
需要熟练掌握 Pear Admin Flask， 否则无法进行开发


4
修改权限管理之后重新登陆生效


5
view/system/rights.py 可以修改部分设置
config.py 可以修改部分设置


6
管理员用户最多为100个，不可以多





```














## 其他

```
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1062, "Duplicate entry '1' for key 'PRIMARY'")
mysql 主键不可以设置为0


@bp.get('/show/')
show 后要加 / 否则会报错

循环引用导致出错
```










