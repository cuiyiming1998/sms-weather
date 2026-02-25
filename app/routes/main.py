from flask import jsonify, Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return jsonify({'message': 'Hello from sms-weather!'})


@bp.route('/health')
def health():
    return jsonify({'status': 'healthy'})
