"""
该脚本演示了如何使用uiautomator2库连接Android设备，
获取设备信息并截图。
这是一个简单的示例，用于测试设备连接和基本功能。
"""

import uiautomator2 as u2  # 导入uiautomator2库，用于控制Android设备
device = u2.connect("127.0.0.1:62025")  # 通过IP和端口连接设备
device.screenshot("test.png")  # 截图并保存为test.png


