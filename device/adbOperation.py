"""
==========================
ADB操作模块
==========================

该模块提供了与ADB（Android Debug Bridge）交互的功能，用于：
- 连接Android设备
- 重启ADB服务
- 向设备发送文本内容
- 切换输入法
等操作
"""

import subprocess  # 用于执行系统命令
import uiautomator2 as u2  # 用于连接和控制Android设备
from config.read_config import readConf 
import logging

class ADBOperation:
    """
    ADB操作类
    提供与ADB交互的各种方法
    """
    
    def connect_device(self, devicename):
        """
        连接Android设备
        
        :param deviceAddress: 设备地址，格式为IP:端口，如"192.168.1.100:5555"
        """
        # 检查设备是否已连接
        connect_result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
        if devicename not in str(connect_result):
            print("There was an error connecting to the device,connect to the device now !!!")
            logging.info("There was an error connecting to the device,connect to the device now !!!")
            # 连接设备
            subprocess.run(["adb", "connect", devicename])
        else:
            
            logging.info("Successfully connected to the device!")

    def reboot_adb(self):
        """
        重启ADB服务
        
        当ADB服务出现问题时，可以通过重启服务来解决
        """
        subprocess.run(["adb", "kill-server"])  # 关闭ADB服务
        subprocess.run(["adb", "start-server"])  # 启动ADB服务

    def send_content_to_device(self, content, devicename=None):
        """
        向设备发送文本内容
        
        :param content: 要发送的文本内容
        :param devicename: 设备名称，如果有多个设备连接时需要指定，默认为None
        """
        try:
            # 构造 ADB 命令
            command = ["adb"]
            if devicename:
                command.extend(["-s", devicename])  # 指定设备
            command.extend(["shell", "input", "text", content])  # 输入文本命令

            # 执行命令
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print("文本输入失败！")
            logging.error("文本输入失败！")
            print("错误信息:", e.stderr)
            logging.error(f"错误信息: {e.stderr}")

    def change_to_next_input_table(self, devicename=None):
        """
        切换到下一个输入法/输入框
        
        通过发送keyevent 61（TAB键）实现切换到下一个输入框
        
        :param devicename: 设备名称，如果有多个设备连接时需要指定，默认为None
        """
        try:
            command = ["adb"]
            if devicename:
                command.extend(["-s", devicename])  # 指定设备
            command.extend(["shell", "input", "keyevent", "61"])  # 发送TAB键事件
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print("错误信息：", e.stderr)
            logging.error(f"错误信息：{e.stderr}")
    
    def clear_app_data(self):
        """
        清除指定应用的数据
        
        :param package_name: 应用的包名
        :param devicename: 设备名称，如果有多个设备连接时需要指定，默认为None
        """
        devicename = readConf().get_device_info()["deviceName"]
        package_name = readConf().get_device_info()["appPackage"]
        try:
            command = ["adb"]
            if devicename:
                command.extend(["-s", devicename])  # 指定设备
            command.extend(["shell", "pm", "clear", package_name])  # 清除应用数据命令
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            print(f"应用 {package_name} 的数据已清除。")
            logging.info(f"应用 {package_name} 的数据已清除。")
        except subprocess.CalledProcessError as e:
            print(f"清除应用 {package_name} 数据失败！")
            logging.error(f"清除应用 {package_name} 数据失败！")
            print("错误信息：", e.stderr)
            logging.error(f"错误信息：{e.stderr}")





if __name__ == '__main__':
    adb = ADBOperation()
    # adb.connect_device("172.16.22.242:5555")
    device_info = ["30019664","3016946","11026472","https://gtt-euser-v6-sit.vdemosit.com","9d9KEJgwIgGBJcgnm65DAE2+0259onUJiYQkQoRRJjs="]
    for i in device_info:
        adb.send_content_to_device(i,"172.16.22.242:5555")
        adb.change_to_next_input_table()
    # adb.change_to_next_input_table()
    # d = u2.connect("172.16.22.242:5555")
    # print(d)
    # logging.info(d)
