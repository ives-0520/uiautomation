import logging
import time
from element_manage.elementOption import ElementOption
from database.excute_sql import EnduserDatabase

class obj_register(ElementOption):
    """
    注册页对象类，基于ElementLocatorManager管理元素
    Registration page object class, based on ElementLocatorManager for element management
    """
    def __init__(self, device, manager):
        """
        初始化注册页对象
        Initialize registration page object
        :param device: 设备对象 / Device object
        :param manager: 元素定位管理器 / Element locator manager
        """
        super().__init__(device)
        self.manager = manager

    def register(self, email, verification_code= None , password= "123456"):
        """
        完整的注册流程，自动化执行所有注册步骤
        Complete registration process, automated execution of all registration steps
        :param email: 邮箱地址 / Email address
        :param verification_code: 验证码 / Verification code
        :param password: 密码 / Password
        """
        try:
            logging.info("Starting registration process")
            
            # 1. 点击注册按钮
            self.click_(self.manager.get_locator("sign_up_tv2").locator)
            logging.info("Successfully clicked register button")
            time.sleep(1)
            
            # 2. 输入邮箱
            self.click_(self.manager.get_locator("layout_email_view").locator["xpath"])
            self.enter_(self.manager.get_locator("layout_email_view").locator["xpath"], email)
            logging.info(f"Successfully input email: {email}")
            time.sleep(1)
            
            # 3. 发送验证码
            self.click_(self.manager.get_locator("tv_verify").locator)
            logging.info("Successfully clicked send verification code button")
            time.sleep(2)  # 等待验证码发送
            
            # 4. 输入验证码

            if not verification_code:
                verification_code = EnduserDatabase().query_unify_verify_code(email)
            self.click_(self.manager.get_locator("et_verify_code").locator)
            self.enter_(self.manager.get_locator("et_verify_code").locator, verification_code)
            logging.info(f"Successfully input verification code: {verification_code}")
            time.sleep(1)
            
            # 5. 输入密码
            self.click_(self.manager.get_locator("et_pwd").locator)
            self.click_(self.manager.get_locator("et_pwd").locator)  # 再次点击确保焦点正确
            self.enter_(self.manager.get_locator("et_pwd").locator, password)
            logging.info("Successfully input password")
            time.sleep(1)
            
            # 6. 提交注册信息
            self.click_(self.manager.get_locator("resetpwd_tv_submit").locator)
            logging.info("Successfully submitted registration information")
            time.sleep(1)
            
            # 7. 同意用户协议
            self.click_(self.manager.get_locator("tv_agreement_agree").locator)
            logging.info("Successfully agreed to terms")
            time.sleep(1)
            
            # 8. 完成注册
            self.click_(self.manager.get_locator("btn_down").locator)
            logging.info("Successfully completed registration")
            
            logging.info("Registration process completed successfully")
            
        except Exception as e:
            logging.error(f"Registration process failed: {e}")
            raise