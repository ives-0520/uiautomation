import logging
import time
from element_manage.elementOption import ElementOption

class obj_login(ElementOption):
    """
    登录页对象类，基于ElementLocatorManager管理元素
    """
    def __init__(self, device, manager):
        super().__init__(device)
        self.manager = manager

    def login(self, username, password):
        """
        邮箱登录流程，自动化执行账号输入、密码输入、登录等操作
        :param username: 邮箱账号
        :param password: 登录密码
        """
        self.click_(self.manager.get_locator("account_login_tv2").locator)
        self.click_(self.manager.get_locator("loginf_et_username").locator)
        self.enter_(self.manager.get_locator("loginf_et_username").locator, username)
        self.click_(self.manager.get_locator("et_pwd").locator)
        self.enter_(self.manager.get_locator("et_pwd").locator, password)
        self.click_(self.manager.get_locator("remember_pwd_cb").locator)
        
       
        self.click_(self.hybrid_loadelement(self.manager.get_locator("loginf_tv_login")))
        
