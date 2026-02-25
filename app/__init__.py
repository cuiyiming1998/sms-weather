from flask import Flask


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object("app.config.Config")

    # 注册路由
    from app.routes import bp

    app.register_blueprint(bp)

    # 注册错误处理器
    from app.routes.errors import register_error_handlers

    register_error_handlers(app)

    return app
