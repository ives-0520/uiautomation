import os
from element_locator_manager import ElementLocatorManager

if __name__ == '__main__':
    # 假设包名和版本
    packagename = 'com.example.demo'
    version = 'v1'
    # 元素库json路径
    locator_path = os.path.join(os.path.dirname(__file__), 'element_locators.json')
    # 初始化管理器
    manager = ElementLocatorManager(locator_path, packagename, version)

    # 要查找的元素名
    element_name = 'loginf_et_username'
    # 获取定位器
    locator = manager.get_locator(element_name)
    if locator:
        print(f"找到传统/AI定位: {locator.to_dict()}")
    else:
        print("未找到定位，尝试AI重定位...")
        ai_locator = manager.try_ai_relocate_and_update(element_name)
        if ai_locator:
            print(f"AI重定位成功: {ai_locator.to_dict()}")
        else:
            print("AI重定位失败")
