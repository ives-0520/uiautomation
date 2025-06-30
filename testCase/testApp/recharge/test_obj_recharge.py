# filepath: c:\Users\Administrator\Desktop\APP_UI_AUTO\testCase\testApp\recharge\test_obj_recharge.py
import logging
import os
import pytest
import allure
import time
from ai.ai_tools import ImageAI
from page_obj.obj_recharge import obj_recharge
from page_obj.obj_login import obj_login

# 示例数据，可根据实际情况替换为外部数据文件  # Example data, can be replaced with external data file
recharge_test_data = [
    ("0609@ipwangxin.cn", "123456", "0032585037446681"),
    # ("otheruser", "otherpassword", "othercode"), # 可添加更多测试数据
]

@allure.story("充值功能")  # Recharge feature
@pytest.mark.parametrize("username, password, code", recharge_test_data)
def test_recharge_flow(app_init, username, password, code):
    device = app_init[0]
    app = app_init[1]
    app.startApp()
    time.sleep(3)
    manager = app_init[3]
    # 登录  # Login
    login_obj = obj_login(device, manager)
    login_obj.login(username, password)
    app.click_(app.manager.get_locator("imageView").locator )
    
    # 充值  # Recharge
    recharge_obj = obj_recharge(device, manager)
    recharge_obj.recharge_flow(code)
    time.sleep(2.5)  # 等待充值流程完成  # Wait for recharge process to complete
    # 充值后截图保存  # Save screenshot after recharge
    case_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_dir = os.path.join(case_dir, "images")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(
        screenshot_dir, f"screenshot_recharge_{time.strftime('%Y%m%d_%H%M%S')}.png"
    )
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    device.screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name="充值后截图", attachment_type=allure.attachment_type.PNG)
    # 断言：检查页面是否有充值成功后的元素（如头像或其他标志性元素）  # Assertion: Check if recharge success element exists
    # assert recharge_obj.is_el_exists(recharge_obj.manager.get_locator("imageView").locator), "断言失败"  # Assertion failed
    locator = ImageAI()
    assert_result=locator.ai_assert(screenshot_path, "判断是否充值成功，并返回判断结果成功或失败，若失败，附上失败原因")  # Determine if recharge is successful, return result or reason
    logging.info(f"充值结果: {assert_result}")  # Log recharge result
    assert "成功" in assert_result, f"充值流程断言失败，{assert_result}"  # Assertion failed if not successful