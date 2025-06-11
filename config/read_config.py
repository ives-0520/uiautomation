"""
==========================
Author:Anthony.zhou
Time: 14:43
===========================

配置读取模块
该模块用于读取config.ini配置文件中的各种配置信息，包括：
- 测试用例Excel文件路径
- 数据库连接信息
- 设备信息
- 应用信息
等
"""

import configparser  # 用于解析配置文件
import os  # 用于文件路径操作
import logging

# 获取项目根目录路径
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置文件路径
conf_path = root_path + r"\config\config.ini"
# 创建配置解析器
conf = configparser.ConfigParser()


class readConf:
    """
    配置读取类
    用于获取config.ini文件中的各种配置信息，如：
    - 测试用例Excel文件路径和工作表名称
    - 要执行的测试用例编号列表
    - 数据库连接信息
    - 设备信息
    - Appium服务器URL
    - 应用信息
    """

    def get_book_path(self):
        """
        获取测试用例Excel文件的完整路径
        :return: Excel文件的绝对路径
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        relativePath = eval(conf.get("workbook", "relativePath"))
        bookPath = str(root_path)+relativePath
        return bookPath

    def get_sheetname(self):
        """
        获取测试用例Excel文件中的工作表名称
        :return: 工作表名称
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        sheetname = eval(conf.get("workbook","sheetname"))
        return sheetname

    def get_projcet_id(self):
        """
        获取测试用例Excel文件中的工作表名称
        :return: 工作表名称
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        sheetname = eval(conf.get("workbook","project_id"))
        return sheetname

    def get_plan_id(self):
        """
        获取测试用例Excel文件中的工作表名称
        :return: 工作表名称
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        sheetname = eval(conf.get("workbook","plan_id"))
        return sheetname

    def get_module(self):
        """
        获取要执行的测试用例编号列表
        :return: 测试用例编号列表
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        testcase_list = eval(conf.get("testcaseNumber","testcase_list"))
        return testcase_list

    def get_database_info(self,dabatase_name):
        """
        获取数据库连接信息
        :return: 包含数据库连接参数的字典
        """
        global conf
        conf.read(conf_path,encoding="utf8")
        dbInfo = eval(conf.get("database","db_dict"))
        if dabatase_name == "euser":
            dbInfo['database'] = eval(conf.get("database","database_euser"))
        elif dabatase_name == "oper":
            dbInfo['database'] = eval(conf.get("database","database_oper"))
        elif dabatase_name == "test_db_sit":
            dbInfo['database'] = eval(conf.get("database","database_test_sit"))

        return dbInfo

    def get_device_info(self):
        """
        获取设备信息
        :return: 包含设备信息的字典，如平台名称、版本、设备名等
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        deviceinfo = eval(conf.get("DeviceInfo","disired_caps"))
        return deviceinfo

    def get_appium_url(self):
        """
        获取Appium服务器URL
        :return: Appium服务器URL
        """
        global conf
        conf.read(conf_path, encoding="utf8")
        appium_url = eval(conf.get("DeviceInfo", "appium_server"))
        return appium_url

    # def get_appinfo(self):
    #     """
    #     获取应用信息
    #     :return: 包含应用信息的字典，如品牌ID、应用ID等
    #     """
    #     global conf
    #     conf.read(conf_path, encoding="utf8")
    #     appinfomation = eval(conf.get("AppInfo", "appinf"))
    #     return appinfomation




if __name__ == '__main__':
    re = readConf().get_book_path()
    # path = readConf().get_book_path()
    # db = readConf().get_database_info()
    # app = readConf().get_appinfo()
    # sheet = readConf().get_sheetname()
    result = readConf().get_module()
    logging.info(result)
