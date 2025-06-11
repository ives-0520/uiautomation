import os
import base64
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
                        {"type": "text", "text": "查找并返回"+prompt+"按钮相对于图片的等比例的元素定位（x，y）坐标，格式固定为(x,y),x，y均为小于1的数"},
                    ],
                }
            ],
        )
        return response.choices[0].message.content

# 使用示例
# locator = ImageLocator()
# result = locator.locate("ai_fallback_1749620940.png", "查找并返回登录按钮相对于图片的等比例的元素定位（x，y）坐标")
# logging.info(result)