"""
测试夹具模块
该模块定义了各种pytest夹具(fixtures)，用于测试前的准备工作和测试后的清理工作。
包括应用初始化、设备连接、数据准备等功能。
"""

import pytest  # 用于测试框架
import subprocess  # 用于执行系统命令
from script.adbOperation import ADBOperation  # 导入ADB操作类
from config.read_config import readConf  # 导入配置读取类
from page_obj import device_init  # 导入设备初始化模块
import os  # 用于文件和目录操作
import logging

log_process = None  # 全局变量，用于保存adb logcat子进程对象
deviceInfo = readConf().get_device_info()  # 读取设备配置信息
deviceName = deviceInfo["deviceName"]  # 获取设备名称

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    在每个测试用例开始前启动 adb logcat，并清空设备日志。
    日志输出到 测试用例文件同级目录下 logs/device_logs/用例名.log 文件。
    同时设置pytest日志文件handler，输出到 logs/pytest_logs/用例名_pylog.txt。
    """
    global log_process
    # 获取当前测试用例文件的目录
    case_dir = os.path.dirname(item.fspath)
    # 构造 logs/device_logs 目录
    log_dir = os.path.join(case_dir, "logs", "device_logs")
    os.makedirs(log_dir, exist_ok=True)
    # 构造 logs/pytest_logs 目录
    pylog_dir = os.path.join(case_dir, "logs", "pytest_logs")
    os.makedirs(pylog_dir, exist_ok=True)
    # 日志文件路径
    log_file = os.path.join(log_dir, f"{item.name}.log")
    pylog_file = os.path.join(pylog_dir, f"{item.name}_pylog.txt")
    # --- 重定向print到pytest日志文件 ---
    import sys
    item._original_stdout = sys.stdout
    item._original_stderr = sys.stderr
    log_file_obj = open(pylog_file, "a", encoding="utf-8")
    item._log_file_obj = log_file_obj
    sys.stdout = log_file_obj
    sys.stderr = log_file_obj
    # 清空设备上的logcat日志
    subprocess.run(["adb", "-s", deviceName, "logcat", "-c"], check=True)
    # 启动 adb logcat，将日志写入文件（覆盖写入模式）
    log_process = subprocess.Popen(
        ["adb", "-s", deviceName, "logcat", "-v", "time"],
        stdout=open(log_file, "w"),  # 'w' 模式覆盖写入
        stderr=subprocess.STDOUT
    )
    logging.info(f"Started adb logcat for test case: {item.name}, log path: {log_file}")
    # 配置pytest日志文件handler（覆盖写入模式）
    logger = logging.getLogger()
    # 移除旧的文件handler，避免重复写入
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
    file_handler = logging.FileHandler(pylog_file, mode='w', encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    在每个测试用例结束后停止 adb logcat，并移除pytest日志文件handler。
    """
    import sys
    global log_process
    logger = logging.getLogger()
    # 移除所有 FileHandler（只移除本次加的）
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
    # 恢复stdout/stderr
    if hasattr(item, "_original_stdout"):
        sys.stdout = item._original_stdout
    if hasattr(item, "_original_stderr"):
        sys.stderr = item._original_stderr
    if hasattr(item, "_log_file_obj"):
        item._log_file_obj.close()
    if log_process:
        log_process.terminate()  # 终止adb logcat进程
        log_process.wait()       # 等待进程完全退出
        logging.info(f"Stopped adb logcat for test case: {item.name}")

@pytest.fixture
def app_init():
    """
    测试用例初始化夹具。
    连接设备，初始化应用对象，测试结束后清理应用数据并关闭应用。
    返回(driver, app, 配置对象)元组。
    """
    global deviceName
    r = readConf()  # 创建配置读取对象
    adb = ADBOperation()  # 创建ADB操作对象
    adb.connect_device(deviceName)  # 连接设备
    driver = device_init.d  # 获取设备对象
    app = device_init.appOpt(driver)  # 创建应用操作对象
    deviceName = device_init.deviceName  # 获取设备名称
    app_packageName = device_init.packageName  # 获取应用包名

    # 返回设备对象、应用操作对象和配置对象
    yield (driver, app, r)

    # 测试完成后清理工作
    # 清除应用数据
    subprocess.run("adb -s {} shell pm clear {} ".format(deviceName, app_packageName), shell=True, check=True)
    # 停止应用
    app.stopApp()




