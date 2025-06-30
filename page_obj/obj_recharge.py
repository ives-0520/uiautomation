import logging
import time
from element_manage.elementOption import ElementOption

class obj_recharge(ElementOption):
    """
    充值页对象类，基于ElementLocatorManager管理元素
    """
    def __init__(self, device, manager):
        super().__init__(device)
        self.manager = manager

    def recharge_flow(self, code):
        """
        充值流程：点击充值入口，输入充值码，点击确认充值按钮。
        :param code: 充值码
        """
        self.click_(self.manager.get_locator("recharge_recycler_view").locator["xpath"])
        self.click_(self.manager.get_locator("recharge_recycler_view").locator["xpath"])
        self.click_(self.manager.get_locator("et_recharge_code").locator)
        self.enter_(self.manager.get_locator("et_recharge_code").locator, code)
        self.click_(self.manager.get_locator("recharge_code_confirm").locator)
        self.click_(self.manager.get_locator("recharge_code_confirm").locator)
