import os
from flask import Flask


def create_app(test_config=None):
    # 创建和配置app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
    )

    if test_config is None:
        # 在不测试时加载实例配置（存在时）
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 否则加载测试配置
        app.config.from_mapping(test_config)

    # 确认目录的存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 简单的路由
    @app.route('/hi')
    def hello():
        return 'Hi, World!'

    from . import db
    # 调用db 并注册数据相关函数
    db.init_app(app)

    from . import auth
    # 注册人脸蓝图
    app.register_blueprint(auth.bp)

    from . import blog
    # 注册博客蓝图
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
