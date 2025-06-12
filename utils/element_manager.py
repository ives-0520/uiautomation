"""
元素定位管理工具
"""
import json
import os
from typing import Dict, Any, List

TEMP_FILE = r"c:\\Users\\Administrator\\Desktop\\APP_UI_AUTO\\temp_element_changes.json"
ELEMENT_DB = r"c:\\Users\\Administrator\\Desktop\\APP_UI_AUTO\\element_db.json"

def save_ai_element_to_temp(element_info: Dict[str, Any]):
    """将AI定位信息写入临时文件"""
    temp_data = []
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, 'r', encoding='utf-8') as f:
            try:
                temp_data = json.load(f)
            except Exception:
                temp_data = []
    temp_data.append(element_info)
    with open(TEMP_FILE, 'w', encoding='utf-8') as f:
        json.dump(temp_data, f, ensure_ascii=False, indent=2)

def update_element_db_from_temp():
    """用例通过时，将临时文件内容批量更新到元素库"""
    if not os.path.exists(TEMP_FILE):
        return
    with open(TEMP_FILE, 'r', encoding='utf-8') as f:
        temp_data = json.load(f)
    db_data = []
    if os.path.exists(ELEMENT_DB):
        with open(ELEMENT_DB, 'r', encoding='utf-8') as f:
            try:
                db_data = json.load(f)
            except Exception:
                db_data = []
    # 合并去重（以element_id为唯一标识）
    db_dict = {item['element_id']: item for item in db_data}
    for item in temp_data:
        db_dict[item['element_id']] = item
    with open(ELEMENT_DB, 'w', encoding='utf-8') as f:
        json.dump(list(db_dict.values()), f, ensure_ascii=False, indent=2)
    os.remove(TEMP_FILE)

def update_element_db_on_fail(failed_element_id: str):
    """用例失败且定位失败时，将AI定位信息更新到元素库"""
    if not os.path.exists(TEMP_FILE):
        return
    with open(TEMP_FILE, 'r', encoding='utf-8') as f:
        temp_data = json.load(f)
    ai_info = None
    for item in temp_data:
        if item['element_id'] == failed_element_id:
            ai_info = item
            break
    if ai_info is None:
        return
    db_data = []
    if os.path.exists(ELEMENT_DB):
        with open(ELEMENT_DB, 'r', encoding='utf-8') as f:
            try:
                db_data = json.load(f)
            except Exception:
                db_data = []
    db_dict = {item['element_id']: item for item in db_data}
    db_dict[failed_element_id] = ai_info
    with open(ELEMENT_DB, 'w', encoding='utf-8') as f:
        json.dump(list(db_dict.values()), f, ensure_ascii=False, indent=2)
    # 可选：移除已处理的临时数据
    temp_data = [item for item in temp_data if item['element_id'] != failed_element_id]
    with open(TEMP_FILE, 'w', encoding='utf-8') as f:
        json.dump(temp_data, f, ensure_ascii=False, indent=2)

# 元素信息结构示例
# {
#   "element_id": "login_button",
#   "ai_locator": "//*[@text='登录']",
#   "attributes": {"text": "登录", "class": "android.widget.Button"},
#   "screenshot": "base64img...",
#   "timestamp": "2024-06-01T12:00:00"
# }

# 元素库文件（element_db.json）结构为元素信息的列表
# [
#   {"element_id": "login_button", ...},
#   {"element_id": "username_input", ...}
# ]
