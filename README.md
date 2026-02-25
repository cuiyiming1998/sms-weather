# SMS Weather 🌤️

> 基于 AI 的智能天气短信服务 - 为你的小仙女送上元气满满的早安天气提醒

## ✨ 功能特性

- 🌤️ **实时天气数据** - 接入彩云天气 API，获取精准的实时天气信息
- 🤖 **AI 智能生成** - 使用智谱 AI 生成甜美软萌的天气短信
- 📱 **iOS 快捷指令** - 完美支持 iOS 快捷指令，自动化发送短信
- 🎯 **精准定位** - 支持自定义城市，默认河北省秦皇岛市
- 🚀 **快速响应** - 使用 GLM-5 模型，秒级生成天气短信

## 📋 项目结构

```
sms-weather/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── config/              # 配置模块
│   │   ├── __init__.py
│   │   └── config.py        # 配置类定义
│   ├── routes/              # 路由模块
│   │   ├── __init__.py      # 蓝图注册
│   │   ├── main.py          # 主路由
│   │   ├── health.py        # 健康检查
│   │   ├── weather.py       # 天气路由
│   │   ├── sms.py           # 短信路由
│   │   └── errors.py        # 错误处理
│   └── utils/               # 工具模块
│       ├── __init__.py
│       ├── response.py      # 统一响应
│       └── ai.py            # AI 功能模块
├── .env                     # 环境变量（需自行创建）
├── .env.example             # 环境变量模板
├── main.py                  # 应用入口
├── pyproject.toml           # 项目配置
└── uv.lock                  # 依赖锁文件
```

## 🚀 快速开始

### 环境要求

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) - 快速的 Python 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone git@github.com:cuiyiming1998/sms-weather.git
cd sms-weather
```

2. **安装依赖**
```bash
uv sync
```

3. **配置环境变量**

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：
```bash
# 彩云天气 API 配置
CAIYUN_API_TOKEN=你的彩云天气API_Token

# 智谱 AI API 配置
ZAI_API_KEY=你的智谱AI_API_KEY
```

4. **启动服务**
```bash
uv run python main.py
```

服务将在 `http://localhost:5999` 启动。

## 🔑 获取 API 密钥

### 彩云天气 API

1. 访问 [彩云天气开放平台](https://open.caiyunapp.com/)
2. 注册并登录
3. 创建应用获取 API Token

### 智谱 AI API

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册并登录
3. 获取 API Key

## 📡 API 文档

### 获取实时天气

**请求**
```http
GET /weather/current
```

**查询参数**

| 参数   | 类型    | 默认值 | 说明                     |
| ------ | ------- | ------ | ------------------------ |
| ai     | boolean | true   | 是否启用 AI 生成天气短信 |
| prompt | string  | -      | 自定义 AI 提示词         |

**响应示例**
```json
{
  "city": "河北省秦皇岛",
  "temperature": "15.3°C",
  "condition": "晴",
  "humidity": "45%",
  "wind": "东南风 3级",
  "wind_speed": "3.2m/s",
  "location": {
    "longitude": 119.5996,
    "latitude": 39.9354
  },
  "raw": {
    "skycon": "CLEAR_DAY",
    "temperature": 15.3,
    "humidity": 45.0,
    "wind_speed": 3.2,
    "wind_direction": 135.0
  },
  "ai_message": "今天秦皇岛天气晴朗，温度15°C，东南风3级。适合外出活动，建议穿着轻薄外套哦！"
}
```

### 健康检查

**请求**
```http
GET /health
```

**响应**
```json
{
  "status": "healthy"
}
```

## 📱 iOS 快捷指令配置

### 创建快捷指令

1. **打开 iOS 快捷指令 App**

2. **创建新快捷指令**
   - 点击右上角 `+` 号
   - 选择"添加操作"

3. **添加操作步骤**

   **步骤 1: 获取天气数据**
   - 搜索"获取 URL 内容"
   - URL 填入：`http://你的服务器地址:5999/weather/current`
   - 方法选择：`GET`

   **步骤 2: 发送短信**
   - 搜索"发送消息"
   - 收件人：选择联系人
   - 信息：从步骤 2 获取的内容

4. **设置自动化（可选）**
   - 点击快捷指令右上角 `...`
   - 选择"自动化"
   - 设置触发时间（如每天早上 7:00）
   - 关闭"运行前询问"

### 快捷指令示例配置

```
1. 获取 URL 内容
   URL: http://your-server:5999/weather/current
   方法: GET
   请求头: 无

2. 发送消息
   收件人: 选择联系人
   信息: 字典值 (步骤 2)
```

## 🎨 自定义 AI 提示词

你可以通过 `prompt` 参数自定义 AI 生成的天气短信风格：

```bash
curl "http://localhost:5999/weather/current?prompt=请用幽默的语气生成一条天气短信"
```

默认提示词特点：
- 💕 甜美软萌的语气
- 👗 贴心的穿衣建议
- 🌸 温暖的早安祝福
- ⚠️ 禁止使用 Emoji（适合短信）

## 🔧 配置说明

### 修改默认城市

编辑 `app/config/config.py`：

```python
QINHUANGDAO_LOCATION = {
    "name": "你的城市",
    "province": "省份",
    "longitude": 经度,
    "latitude": 纬度
}
```

### 修改服务端口

编辑 `.env` 文件：

```bash
PORT=5999
```

## 📝 开发说明

### 项目技术栈

- **Web 框架**: Flask 3.1
- **AI 服务**: 智谱 AI (GLM-5)
- **天气 API**: 彩云天气 v2.6
- **包管理**: uv

## 📄 License

MIT License

Made with ❤️ by [cuiyiming1998](https://github.com/cuiyiming1998)
