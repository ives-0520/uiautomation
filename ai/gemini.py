import base64
import os
from google import genai
from google.genai import types
client = genai.Client(api_key="AIzaSyA9SXfG0kORgcsscnu1auCOnchJQEEC5Ag")

 

file_path = os.path.join(os.path.dirname(__file__), "test.png")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
with open(file_path, "rb") as f:
    base64_data = base64.b64encode(f.read()).decode("utf-8")

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
      types.Part.from_bytes(
        data=base64_data,
        mime_type='image/png',
      ),
      '''【任务指令】分析这张APP截图，找到符合以下描述的UI元素：绑定按钮
                  
                【输出要求】请返回：  
                    1. 元素的文本内容（如有）
                    2. 元素在截图中的相对坐标位置（x，y）
                    3. 元素类型（如按钮、文本框、图标等）  
                    4. 模型对识别结果的置信度（0-1之间的数值）  
                    5. 元素与其他UI组件的关系（如是否相邻/包含搜索框）
                    6. 元素描述'''
    ]
  )

print(response.text)