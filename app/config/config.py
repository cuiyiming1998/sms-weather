import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""

    # Flask配置
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # 应用配置
    APP_NAME = "sms-weather"
    APP_VERSION = "0.1.0"

    # 彩云天气API配置
    CAIYUN_API_TOKEN = os.getenv("CAIYUN_API_TOKEN", "")
    CAIYUN_API_BASE_URL = "https://api.caiyunapp.com/v2.6"

    # api key
    ZAI_API_KEY = os.getenv("ZAI_API_KEY", "")

    # 秦皇岛坐标 (河北省)
    QINHUANGDAO_LOCATION = {
        "name": "秦皇岛",
        "province": "河北省",
        "longitude": 119.5996,
        "latitude": 39.9354,
    }
