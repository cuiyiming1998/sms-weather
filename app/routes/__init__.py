from flask import Blueprint

from app.routes.main import bp as main_bp
from app.routes.sms import bp as sms_bp
from app.routes.weather import bp as weather_bp

# 主蓝图
bp = Blueprint('main', __name__)

# 注册子蓝图
bp.register_blueprint(main_bp, url_prefix='/')
bp.register_blueprint(sms_bp, url_prefix='/sms')
bp.register_blueprint(weather_bp, url_prefix='/weather')
