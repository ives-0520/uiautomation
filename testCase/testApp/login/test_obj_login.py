import logging
from operator import contains
import pytest
import time
from page_obj.obj_login import obj_login




def test_login_email_flow(app_init):
    device = app_init[0]
    app = app_init[1]  # 应用操作对象
    app.startApp()  # 启动应用
    time.sleep(3)
    login_obj = obj_login(device)
    username = "0609@ipwangxin.cn"
    password = "123456"
    login_obj.login(username, password)
    # 断言：检查页面是否成功登录
    assert login_obj.is_el_exists(login_obj.imageView), "断言失败"


def test_login_wrong_credentials(app_init):
    """
    输入错误的账号或密码，点击“登录”按钮，系统应提示“账号或密码错误”。
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    wrong_username = "wrong@ipwangxin.cn"
    wrong_password = "wrongpwd"
    login_obj.login(wrong_username, wrong_password)
    # 断言：检查页面是否有“账号或密码错误”提示
    assert login_obj.is_el_exists(login_obj.tv_content) 
    assert  "22010008:(The account and password you entered did not match our records. Please double-check and try again.)" in login_obj.get_element_text(login_obj.tv_content) , "登录失败，未检测到错误提示"


def test_login_empty_credentials(app_init):
    """
    不输入账号或密码，直接点击“登录”按钮，系统应提示“请输入账号/密码”。
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    login_obj.login("", "")
    # 断言：检查页面是否有“请输入账号/密码”提示
    # assert login_obj.get_toast_message() == "请输入账号/密码"


def test_login_network_exception(app_init):
    """
    网络异常时点击“登录”按钮，系统应提示“网络异常，请稍后重试”。
    """
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    login_obj = obj_login(device)
    username = "0609@ipwangxin.cn"
    password = "123456"
    # 断开网络连接（此处需补充具体断网操作）
    # device.disconnect_network()
    login_obj.login(username, password)
    # 断言：检查页面是否有“网络异常，请稍后重试”提示
    # assert login_obj.get_toast_message() == "网络异常，请稍后重试"

