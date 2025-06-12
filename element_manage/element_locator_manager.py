import json
import os
from typing import Dict, Any, Optional
from ElementLocatorSchema import ElementLocator
from config.read_config import readConf
r = readConf()
packagename = r.get_device_info()['appPackage']


def get_highest_version(versions):
    # 假设版本号格式为v1、v2...，按数字排序
    return sorted(versions, key=lambda x: int(x[1:]), reverse=True)[0]

class ElementLocatorManager:
    def __init__(self, locator_json_path: str, packagename: str, version: str):
        # 初始化，加载定位器json文件
        self.packagename = packagename
        self.version = version
        with open(locator_json_path, 'r', encoding='utf-8') as f:
            self.locators: Dict[str, Any] = json.load(f)

    def get_locator(self, name: str) -> Optional[ElementLocator]:
        # 获取指定元素名的定位器
        element = self.locators.get(name)
        if not element:
            return None
        # 优先查找指定版本
        version_dict = element.get(self.version)
        if not version_dict:
            # 没有指定版本，取最高版本
            highest_version = get_highest_version(element.keys())
            version_dict = element[highest_version]
        # 优先traditional
        if 'traditional' in version_dict:
            locator_data = version_dict['traditional']
            locator_data = self._replace_packagename(locator_data)
            return ElementLocator.from_dict(locator_data)
        # 没有traditional，尝试ai
        if 'ai' in version_dict:
            locator_data = version_dict['ai']
            locator_data = self._replace_packagename(locator_data)
            return ElementLocator.from_dict(locator_data)
        return None

    def try_ai_relocate_and_update(self, name: str):
        # 尝试AI重定位并更新到json
        ai_locator = self._call_ai_relocate(name)
        if ai_locator:
            # 更新到json结构
            element = self.locators.setdefault(name, {})
            version_dict = element.setdefault(self.version, {})
            version_dict['ai'] = ai_locator
            # 持久化到文件
            self._save()
            return ElementLocator.from_dict(ai_locator)
        return None

    def _replace_packagename(self, locator_data):
        # 替换locator中的{packagename}为实际包名，并补充version字段
        locator = locator_data.get('locator', {})
        locator_str = json.dumps(locator)
        locator_str = locator_str.replace('{packagename}', self.packagename)
        locator_data = locator_data.copy()
        locator_data['locator'] = json.loads(locator_str)
        # 补充version字段
        locator_data['version'] = self.version
        return locator_data

    def _call_ai_relocate(self, name: str):
        # 伪AI重定位，实际应调用AI服务
        # 返回格式应与ai定位结构一致
        return {
            "description": f"AI重定位的{name}",
            "locator": {"ai_key": f"ai_locator_for_{name}"},
            "ai_fields": {"confidence": 0.99}
        }

    def _save(self):
        # 保存到json文件
        with open(os.path.join(os.path.dirname(__file__), 'element_locators.json'), 'w', encoding='utf-8') as f:
            json.dump(self.locators, f, ensure_ascii=False, indent=4)

# 用法示例
if __name__ == '__main__':
    packagename = 'com.example.demo'
    version = 'v1'
    locator_path = os.path.join(os.path.dirname(__file__), 'element_locators.json')
    manager = ElementLocatorManager(locator_path, packagename, version)
    element_name = 'loginf_et_username'
    locator = manager.get_locator(element_name)
    if locator:
        print(f"传统/AI定位: {locator.locator}")
    else:
        print("未找到定位，尝试AI重定位...")
        ai_locator = manager.try_ai_relocate_and_update(element_name)
        if ai_locator:
            print(f"AI重定位成功: {ai_locator.locator}")
        else:
            print("AI重定位失败")
