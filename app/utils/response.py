from flask import jsonify
from typing import Any, Optional


def success_response(
    data: Any = None, message: str = "success", code: int = 200, raw: bool = False
):
    """成功响应

    Args:
        data: 响应数据
        message: 响应消息
        code: HTTP状态码
        raw: 是否直接返回原始数据（不包装）
    """

    if raw:
        return jsonify(data), code

    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), code


def error_response(message: str, code: int = 400, error: Optional[str] = None):
    """错误响应"""
    response = {"success": False, "message": message}
    if error:
        response["error"] = error
    return jsonify(response), code
