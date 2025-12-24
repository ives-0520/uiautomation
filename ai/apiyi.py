from openai import OpenAI
import os
import base64

file_path = os.path.join(os.path.dirname(__file__), "test.png")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
with open(file_path, "rb") as f:
    base64_data = base64.b64encode(f.read()).decode("utf-8")

client = OpenAI(
    api_key="sk-qIPVIy4RR6qGov2q48E10908C5874757A82bC39d0d84CbD6",
    base_url="https://api.apiyi.com/v1"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash-001",
    messages=[
        {"role": "user", "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_data}"
                }
            },
            {
                "type": "text",
                "text": '''【任务指令】分析这张APP截图，找到符合以下描述的UI元素：绑定按钮
                  
                【输出要求】请返回：  
                    1. 元素的文本内容（如有）
                    2. 元素在截图中的相对坐标位置（x，y）
                    3. 元素类型（如按钮、文本框、图标等）  
                    4. 模型对识别结果的置信度（0-1之间的数值）  
                    5. 元素与其他UI组件的关系（如是否相邻/包含搜索框）
                    6. 元素描述'''
            }
        ]}
    ]
    
)

print(response.choices[0].message.content)