import requests
from flask import jsonify, Blueprint, request, current_app

from app.utils.response import success_response, error_response
from app.utils.ai import get_ai_result

bp = Blueprint("weather", __name__)


def get_weather_skycon(skycon: str) -> str:
    """将天气状况代码转换为中文描述"""
    skycon_map = {
        "CLEAR_DAY": "晴",
        "CLEAR_NIGHT": "晴",
        "PARTLY_CLOUDY_DAY": "多云",
        "PARTLY_CLOUDY_NIGHT": "多云",
        "CLOUDY": "阴",
        "LIGHT_HAZE": "轻雾",
        "MODERATE_HAZE": "中雾",
        "HEAVY_HAZE": "重雾",
        "LIGHT_RAIN": "小雨",
        "MODERATE_RAIN": "中雨",
        "HEAVY_RAIN": "大雨",
        "STORM_RAIN": "暴雨",
        "LIGHT_SNOW": "小雪",
        "MODERATE_SNOW": "中雪",
        "HEAVY_SNOW": "大雪",
        "STORM_SNOW": "暴雪",
        "DUST": "浮尘",
        "SAND": "沙尘",
        "WIND": "大风",
    }
    return skycon_map.get(skycon, "未知")


def get_wind_direction(direction: float) -> str:
    """将风向角度转换为文字描述"""
    if direction >= 337.5 or direction < 22.5:
        return "北风"
    elif 22.5 <= direction < 67.5:
        return "东北风"
    elif 67.5 <= direction < 112.5:
        return "东风"
    elif 112.5 <= direction < 157.5:
        return "东南风"
    elif 157.5 <= direction < 202.5:
        return "南风"
    elif 202.5 <= direction < 247.5:
        return "西南风"
    elif 247.5 <= direction < 292.5:
        return "西风"
    else:
        return "西北风"


def get_wind_level(speed: float) -> str:
    """将风速转换为风力等级"""
    if speed < 0.3:
        return "0级"
    elif speed < 1.6:
        return "1级"
    elif speed < 3.4:
        return "2级"
    elif speed < 5.5:
        return "3级"
    elif speed < 8.0:
        return "4级"
    elif speed < 10.8:
        return "5级"
    elif speed < 13.9:
        return "6级"
    elif speed < 17.2:
        return "7级"
    elif speed < 20.8:
        return "8级"
    elif speed < 24.5:
        return "9级"
    elif speed < 28.5:
        return "10级"
    elif speed < 32.7:
        return "11级"
    else:
        return "12级"


@bp.route("/current")
def current():
    """获取当前实时天气"""
    from app.config import Config

    # 获取请求参数
    enable_ai = request.args.get("ai", "true").lower() == "true"
    custom_prompt = request.args.get("prompt", "")

    # 检查API Token
    if not Config.CAIYUN_API_TOKEN:
        return error_response("未配置彩云天气API Token", 500)

    # 获取秦皇岛坐标
    location = Config.QINHUANGDAO_LOCATION
    longitude = location["longitude"]
    latitude = location["latitude"]
    city_name = location["name"]
    province = location["province"]

    # 构建API请求URL
    url = f"{Config.CAIYUN_API_BASE_URL}/{Config.CAIYUN_API_TOKEN}/{longitude},{latitude}/realtime"

    try:
        # 发起API请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 检查API响应状态
        if data.get("status") != "ok":
            return error_response(
                f"天气API返回错误: {data.get('status', 'unknown')}", 500
            )

        # 解析实时天气数据
        realtime = data.get("result", {}).get("realtime", {})

        temperature = realtime.get("temperature", 0)
        humidity = realtime.get("humidity", 0) * 100
        skycon = realtime.get("skycon", "")
        wind = realtime.get("wind", {})
        wind_speed = wind.get("speed", 0)
        wind_direction = wind.get("direction", 0)
        air_quality = realtime.get("air_quality", {}).get("description", {})
        life_index = realtime.get("life_index", {})

        # 构建天气数据
        weather_data = {
            "city": f"{province}{city_name}",
            "location": {"longitude": longitude, "latitude": latitude},
            "temperature": f"{temperature:.1f}°C",
            "condition": get_weather_skycon(skycon),
            "humidity": f"{humidity:.0f}%",
            "wind": f"{get_wind_direction(wind_direction)} {get_wind_level(wind_speed)}",
            "wind_speed": f"{wind_speed:.1f}m/s",
            "air_quality": f"{air_quality.get('usa', '轻度污染')}",
            "comfort": f"{life_index.get('comfort', '一般')}",
            "raw": {
                "skycon": skycon,
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction,
            },
        }

        # 如果启用AI，调用AI生成天气短信
        if enable_ai:
            ai_message = get_ai_result(weather_data, custom_prompt)
            weather_data["ai_message"] = ai_message
            return success_response(data=ai_message, message="获取成功", raw=True)

        return success_response(weather_data, "获取成功")

    except requests.exceptions.RequestException as e:
        return error_response(f"请求天气API失败: {str(e)}", 500)
    except Exception as e:
        return error_response(f"获取天气信息失败: {str(e)}", 500)


@bp.route("/forecast")
def forecast():
    """获取天气预报"""
    city = request.args.get("city", "北京")
    days = request.args.get("days", 3, type=int)
    return jsonify(
        {
            "city": city,
            "days": days,
            "forecast": [
                {
                    "date": "2025-02-25",
                    "high": "28°C",
                    "low": "18°C",
                    "condition": "晴天",
                },
                {
                    "date": "2025-02-26",
                    "high": "26°C",
                    "low": "17°C",
                    "condition": "多云",
                },
                {
                    "date": "2025-02-27",
                    "high": "24°C",
                    "low": "16°C",
                    "condition": "小雨",
                },
            ],
        }
    )
