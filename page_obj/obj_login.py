import time


from page_obj.element_location import Element_Location
from script.elementOption import ElementOption

class obj_login(Element_Location, ElementOption):
    """
    登录页对象类，继承元素定位和元素操作
    """
    def __init__(self, device):
        ElementOption.__init__(self, device)

    
    
    def login(self, username, password):
        """
        邮箱登录流程，自动化执行账号输入、密码输入、登录等操作
        :param username: 邮箱账号
        :param password: 登录密码
        """
        
        self.click_(self.account_login_tv2)
        self.click_(self.loginf_et_username)
        self.enter_(self.loginf_et_username, username)
        self.click_(self.et_pwd)
        self.enter_(self.et_pwd, password)
        self.click_(self.remember_pwd_cb)
        # self.click_(self.loginf_tv_login)
        self.click_(self.hybrid_loadelement(self.loginf_tv_login))
        
        # self.click_((0.576, 0.708))
        # self.click_(self.imageView)
        # self.device.click(0.835, 0.169)

        
