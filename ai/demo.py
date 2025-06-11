import os
import base64
from openai import OpenAI
import logging

# 读取本地文件并转为 Base64
file_path = os.path.join(os.path.dirname(__file__), "test.png")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
with open(file_path, "rb") as f:
    base64_data = base64.b64encode(f.read()).decode("utf-8")

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    # api_key=os.environ.get("ARK_API_KEY"),
    api_key="2bb4e659-145c-44f5-8d7a-13b5959cbe65",
)

response = client.chat.completions.create(
    # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
    model="doubao-1-5-thinking-vision-pro-250428",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_data}"
                    },
                },
                {"type": "text", "text": "查找并返回bind按钮相对于图片的等比例的元素定位（x，y）坐标，只返回坐标不要返回多余的内容"},
            ],
        }
    ],
)

logging.info(response.choices[0].message.content)