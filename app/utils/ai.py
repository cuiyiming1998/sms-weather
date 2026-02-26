from zai import ZhipuAiClient
from app.config import Config

client = ZhipuAiClient(api_key=Config.ZAI_API_KEY)


def get_ai_result(weather_data: dict, prompt: str = "") -> str:
    """
    调用智谱AI处理天气数据

    Args:
        weather_data: 天气数据字典
        prompt: 用户自定义提示词

    Returns:
        AI生成的回复内容
    """
    # 默认提示词
    default_prompt = """# Role
你是一位元气满满、软萌可爱的私人生活助理。你的用户是一位精致的小仙女，你可以称呼她为曦曦，你需要用温柔、俏皮的语气为她生成早安天气提醒。

# Goals
1. 用甜美、像闺蜜聊天一样的语气播报天气。
2. 根据天气提供贴心的穿衣建议，重点考虑保暖、防晒或美美哒穿搭。
3. 附带一句温暖的早安祝福。

# Constraints
- 禁止使用Emoji表情符号（如☀️🌧️👗🧣✨）。
- 语气要软糯，偶尔语气词（呀、呢、哒、哦、啦）。
- 字数控制在100字以内，适合短信发送，不要使用Markdown格式。

# Workflow & Logic
1. **天气解读**：
   - 晴天：夸赞天气好，适合出游，但注意紫外线。
   - 下雨：提醒带伞，语气要像是在担心她淋湿。
   - 降温：用“魔法攻击”、“冻坏小仙女”等可爱词汇强调保暖。
2. **穿衣建议**：
   - 根据不同温度，推荐合适的出行穿衣推荐。
3. **污染及生活指数**:
   - 根据不同的污染情况, 生活指数(air_quality和comfort)，推荐是否需要戴口罩，涂防晒霜等做好防护


4. **生成文本**：将信息串联成一段甜甜的短信。
天气数据：
{weather_data}
"""

    # 使用用户提供的提示词或默认提示词
    final_prompt = prompt if prompt else default_prompt

    # 格式化天气数据
    weather_text = _format_weather_data(weather_data)
    final_prompt = final_prompt.format(weather_data=weather_text)

    try:
        response = client.chat.completions.create(
            model="glm-5",
            messages=[{"role": "user", "content": final_prompt}],
            thinking={"type": "enabled"},
        )
        return response.choices[0].message.content or "AI回复生成失败"  # type: ignore
    except Exception as e:
        return f"AI调用失败: {str(e)}"


def _format_weather_data(data: dict) -> str:
    """格式化天气数据为文本"""
    city = data.get("city", "未知")
    temperature = data.get("temperature", "未知")
    condition = data.get("condition", "未知")
    humidity = data.get("humidity", "未知")
    wind = data.get("wind", "未知")

    return f"""城市：{city}
温度：{temperature}
天气：{condition}
湿度：{humidity}
风力：{wind}"""
