"""
设备初始化模块
该模块用于连接设备并提供应用启动和停止功能。
通过uiautomator2库实现与Android设备的连接和控制。
"""
import time  # 用于延时操作

from config.read_config import readConf  # 导入配置读取类
import uiautomator2 as u2  # 导入uiautomator2库，用于控制Android设备
from script.elementOption import ElementOption
from page_obj.element_location import Element_Location

# 从配置文件获取设备名称和应用包名
deviceName = readConf().get_device_info()["deviceName"]
packageName = readConf().get_device_info()["appPackage"]
# 连接设备
d = u2.connect(deviceName)

class appOpt(ElementOption,Element_Location):
    """
    应用操作类
    提供应用启动和停止功能
    """
    def startApp(self):
        """
        启动应用
        使用全局变量d和packageName启动应用
        """
        global d, packageName
        d.app_start(packageName)
        time.sleep(3)
        if self.loadelement(self.permission_allow_button):
            self.click_(self.permission_allow_button)


    def stopApp(self):
        """
        停止应用
        使用全局变量d和packageName停止应用
        """
        global d, packageName
        d.app_stop(packageName)
    

    











if __name__ == '__main__':
    a = appOpt(d)
    a.startApp()
    time.sleep(5)
    # a.stopApp()
