import os
from flask import Flask
from applications.common.script import init_script
from applications.config import BaseConfig
from applications.extensions import init_plugs
from applications.view import init_bps
from applications.view.front.front import cache as front_cache
from applications.view.student.api import cache as api_cache
from applications.view.student.student import cache as student_cache


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # 引入配置
    app.config.from_object(BaseConfig)

    # 缓存
    # 添加缓存配置
    app.config['CACHE_TYPE'] = 'SimpleCache'


    # 注册flask组件
    init_plugs(app)

    # 缓存
    # 初始化蓝图缓存
    front_cache.init_app(app)
    api_cache.init_app(app)
    student_cache.init_app(app)

    # 注册蓝图
    init_bps(app)

    # 注册命令
    init_script(app)

    return app
