from flask import jsonify, Blueprint, request

bp = Blueprint('sms', __name__)


@bp.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    phone = data.get('phone')
    message = data.get('message')

    if not phone or not message:
        return jsonify({'error': '手机号和消息内容不能为空'}), 400

    return jsonify({
        'success': True,
        'message': '短信发送成功',
        'data': {
            'phone': phone,
            'content': message
        }
    })


@bp.route('/weather', methods=['POST'])
def send_weather():
    data = request.get_json()
    phone = data.get('phone')
    city = data.get('city', '北京')

    if not phone:
        return jsonify({'error': '手机号不能为空'}), 400

    return jsonify({
        'success': True,
        'message': f'已向 {phone} 发送 {city} 的天气短信'
    })
