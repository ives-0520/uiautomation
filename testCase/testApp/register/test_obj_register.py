"""
注册功能测试用例模块
Registration functionality test case module
该模块包含注册流程的各种测试场景，包括正向流程和异常场景测试
This module contains various test scenarios for registration process, including positive and negative test cases
"""

import logging
import os
import json
import allure
import pytest
import time
from page_obj.obj_register import obj_register
import utils.account_generate as account_generate



@allure.story("注册功能")
@allure.title("完整注册流程测试")
@allure.description("测试用户完整的注册流程，包括输入邮箱、发送验证码、输入验证码、设置密码等步骤")
def test_register_complete_flow(app_init):
    """
    完整注册流程测试
    Complete registration flow test
    测试用户从开始到完成的完整注册流程
    Test complete user registration flow from start to finish
    """
    device = app_init[0]  # 获取设备对象 / Get device object
    app = app_init[1]     # 获取应用操作对象 / Get app operation object
    manager = app_init[3] # 获取元素定位管理器 / Get element locator manager
    
    # 启动应用
    app.startApp()
    time.sleep(3)
    
    # 创建注册页面对象
    register_obj = obj_register(device, manager)
    
    # 生成测试数据
    test_email = account_generate.generate_random_email()  # 生成随机邮箱
    
    test_verification_code = "2234"  # 模拟验证码
    
    logging.info(f"开始注册流程测试，邮箱: {test_email}")
    
    try:
        # 执行完整注册流程
        # register_obj.register(test_email, test_verification_code, "123456")
        register_obj.register(test_email)
        
        # 等待注册完成
        time.sleep(3)
        
        # 断言：检查注册是否成功（这里需要根据实际应用的成功标识进行调整）
        # 可以检查是否跳转到登录页面或显示注册成功提示
        logging.info("注册流程执行完成")
        
        # 示例断言，需要根据实际应用调整
        # assert register_obj.is_el_exists(success_indicator), "注册流程未成功完成"
        
    except Exception as e:
        logging.error(f"注册流程测试失败: {e}")
        # 添加失败时的截图
        allure.attach(
            device.screenshot(),
            name="注册失败截图",
            attachment_type=allure.attachment_type.PNG
        )
        raise



  