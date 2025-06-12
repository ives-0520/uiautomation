import os
import base64
import re
from openai import OpenAI
import logging

class ImageLocator:
    def __init__(self, api_key="2bb4e659-145c-44f5-8d7a-13b5959cbe65", base_url="https://ark.cn-beijing.volces.com/api/v3", model="doubao-1-5-thinking-vision-pro-250428"):
        self.api_key = api_key or os.environ.get("ARK_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the ARK_API_KEY environment variable.")
        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key,
        )
        self.model = model

    def locate(self, image_path, prompt):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
        with open(image_path, "rb") as f:
            base64_data = base64.b64encode(f.read()).decode("utf-8")
        response = self.client.chat.completions.create(
            model=self.model,
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
                        # {"type": "text", "text": "查找并返回"+prompt+"按钮相对于图片的等比例的元素定位（x，y）坐标，格式固定为(x,y),x，y均为小于1的数"},
                        {
                            "type": "text", 
                            "text":f"""
                            【任务指令】分析这张APP截图，找到符合以下描述的UI元素：{prompt}
                            
                            【输出要求】请返回：  
                                1. 元素的文本内容（如有）
                                2. 元素在截图中的相对坐标位置（x，y）,格式为 (x, y)，x、y均为小于1的数
                                3. 元素类型（如按钮、文本框、图标等）  
                                4. 模型对识别结果的置信度（0-1之间的数值）  
                                5. 元素与其他UI组件的关系（如是否相邻/包含搜索框）
                                6. 元素描述
                                
                            """
                        }
                    ],
                }
            ],
        )
        logging.info(f"AI定位返回信息: {response}")
        return response.choices[0].message.content
    



    def extract_relative_coordinates(self,ai_response: str) -> tuple:
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


    def extract_element_text(self, ai_response: str, element: str) -> str:
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


# 使用示例
# locator = ImageLocator()
# result = locator.locate("ai_fallback_1749620940.png", "查找并返回登录按钮相对于图片的等比例的元素定位（x，y）坐标")
# logging.info(result)