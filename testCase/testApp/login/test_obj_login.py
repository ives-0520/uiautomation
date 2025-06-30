# filepath: c:\Users\Administrator\Desktop\APP_UI_AUTO\testCase\testApp\login\test_obj_login.py

import logging
import os
import json
from operator import contains
import allure
import pytest
import time
from page_obj.obj_login import obj_login

# 加载外部测试数据  # Load external test data
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data\login_test_data.json')
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    test_data = json.load(f)



@allure.story("登录功能")
def test_login_email_flow(app_init):
    device = app_init[0]
    app = app_init[1]  # 应用操作对象
    app.startApp()  # 启动应用
    time.sleep(3)
    manager =app_init[3]  # 获取元素定位管理器
    login_obj = obj_login(device, manager)
    username = test_data["valid_user"]["username"]
    password = test_data["valid_user"]["password"]
    login_obj.login(username, password)
    # 断言：检查页面是否成功登录  # Assertion: Check if login is successful
    assert login_obj.is_el_exists(login_obj.manager.get_locator("imageView").locator), "断言失败"  # Assertion failed


def test_login_wrong_credentials(app_init):
    """
    输入错误的账号或密码，点击“登录”按钮，系统应提示“账号或密码错误”。  # Enter wrong username or password, system should prompt error.
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    # 重新初始化manager
    from element_manage.element_locator_manager import ElementLocatorManager
    import os
    manager = app.manager
    from page_obj.obj_login import obj_login
    login_obj = obj_login(device, manager)
    wrong_username = test_data["invalid_user"]["username"]
    wrong_password = test_data["invalid_user"]["password"]
    login_obj.login(wrong_username, wrong_password)
    # 断言：检查页面是否有“账号或密码错误”提示  # Assertion: Check if error message is shown
    assert login_obj.is_el_exists(login_obj.tv_content) 
    assert  "22010008:(The account and password you entered did not match our records. Please double-check and try again.)" in login_obj.get_element_text(login_obj.tv_content) , "登录失败，未检测到错误提示"  # Login failed, error message not detected


def test_login_empty_credentials(app_init):
    """
    不输入账号或密码，直接点击“登录”按钮，系统应提示“请输入账号/密码”。  # No username or password, system should prompt input required.
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    # 重新初始化manager
    from element_manage.element_locator_manager import ElementLocatorManager
    import os
    manager = app.manager
    from page_obj.obj_login import obj_login
    login_obj = obj_login(device, manager)
    login_obj.login(test_data["empty_user"]["username"], test_data["empty_user"]["password"])
    # 断言：检查页面是否有“请输入账号/密码”提示  # Assertion: Check if input required message is shown
    # assert login_obj.get_toast_message() == "请输入账号/密码"


def test_login_network_exception(app_init):
    """
    网络异常时点击“登录”按钮，系统应提示“网络异常，请稍后重试”。  # Network error, system should prompt retry.
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    # 重新初始化manager
    from element_manage.element_locator_manager import ElementLocatorManager
    import os
    manager = app.manager
    from page_obj.obj_login import obj_login
    login_obj = obj_login(device, manager)
    username = test_data["valid_user"]["username"]
    password = test_data["valid_user"]["password"]
    # 断开网络连接（此处需补充具体断网操作）
    # device.disconnect_network()
    login_obj.login(username, password)
    # 断言：检查页面是否有“网络异常，请稍后重试”提示  # Assertion: Check if network error message is shown
    # assert login_obj.get_toast_message() == "网络异常，请稍后重试"

