import os
import base64
import re
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
                {"type": "text", "text":
                 """
                【任务指令】分析这张APP截图，找到符合以下描述的UI元素：绑定按钮
                  
                【输出要求】请返回：  
                    1. 元素的文本内容（如有）
                    2. 元素在截图中的相对坐标位置（x，y）
                    3. 元素类型（如按钮、文本框、图标等）  
                    4. 模型对识别结果的置信度（0-1之间的数值）  
                    5. 元素与其他UI组件的关系（如是否相邻/包含搜索框）
                    6. 元素描述
                    
                """
                }, 
            ],
        }
    ],
)

print(response.choices[0].message.content)



def extract_element_text(ai_response: str, element: str) -> str:
    """
    从AI返回的文本中提取指定元素的文本内容。

    :param ai_response: AI返回的文本内容
    :param element: 需要提取的元素名称
    :return: 元素对应的文本内容，未找到则返回空字符串
    """
    # 适配类似“1. 文本内容：Bind”格式，直接提取“文本内容”字段
    pattern = r"1\.\s*文本内容[：:]\s*(.*)"
    match = re.search(pattern, ai_response)
    if match:
        return match.group(1).strip()
    return ""

def extract_relative_coordinates(ai_response: str) -> tuple:
        """
        从AI返回的文本中提取元素相对坐标 (x, y)，假设格式为 (x, y)，x、y均为小于1的数。

        :param ai_response: AI返回的文本内容
        :return: (x, y) 元组，未找到则返回 None
        """
        match = re.search(r"\(\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)", ai_response)
        if match:
            x = float(match.group(1))
            y = float(match.group(2))
            return (x, y)
        return None

# result=  extract_element_text(response.choices[0].message.content, "绑定按钮")
result=  extract_relative_coordinates(response.choices[0].message.content)
print(f"提取的元素: {result}")


