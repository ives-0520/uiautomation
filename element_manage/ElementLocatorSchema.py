from typing import Optional, Dict, Any

class ElementLocator:
    # 元素定位数据结构类
    def __init__(self, description: str, locator: Dict[str, Any], version: str, locator_type: str = 'traditional', ai_fields: Optional[Dict[str, Any]] = None):
        """
        初始化元素定位对象
        :param description: 元素描述
        :param locator: 元素定位方式（如{"text": "v-demo"}等字典形式）
        :param version: 元素定位版本
        :param locator_type: 定位类型（'traditional' 或 'ai'）
        :param ai_fields: AI定位扩展字段（仅当locator_type为'ai'时使用）
        """
        self.description = description  # 元素描述
        self.locator = locator          # 元素定位方式（字典）
        self.version = version          # 元素定位版本
        self.locator_type = locator_type  # 定位类型
        self.ai_fields = ai_fields or {}  # AI定位扩展字段

    def to_dict(self):
        """
        转换为字典格式，便于序列化存储
        """
        data = {
            'description': self.description,
            'locator': self.locator,
            'version': self.version,
            'type': self.locator_type
        }
        if self.locator_type == 'ai':
            data['ai_fields'] = self.ai_fields  # 仅AI类型包含扩展字段
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """
        从字典数据创建ElementLocator对象
        """
        return ElementLocator(
            description=data.get('description', ''),
            locator=data.get('locator', {}),
            version=data.get('version', ''),
            locator_type=data.get('type', 'traditional'),
            ai_fields=data.get('ai_fields', {})
        )
