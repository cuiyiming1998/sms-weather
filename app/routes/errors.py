from flask import jsonify
from app.utils.response import error_response


def register_error_handlers(app):
    """注册错误处理器"""

    @app.errorhandler(404)
    def not_found(error):
        return error_response('资源不存在', 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response('方法不允许', 405)

    @app.errorhandler(500)
    def internal_error(error):
        return error_response('服务器内部错误', 500)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return error_response(f'未知错误: {str(error)}', 500)
