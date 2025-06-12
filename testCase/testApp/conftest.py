"""
测试夹具模块
该模块定义了各种pytest夹具(fixtures)，用于测试前的准备工作和测试后的清理工作。
包括应用初始化、设备连接、数据准备等功能。
"""
import sys
import pytest  # 用于测试框架
import subprocess  # 用于执行系统命令
from script.adbOperation import ADBOperation  # 导入ADB操作类
from config.read_config import readConf  # 导入配置读取类
from page_obj import device_init  # 导入设备初始化模块
import os  # 用于文件和目录操作
import logging
import allure  # 导入allure

log_process = None  # 全局变量，用于保存adb logcat子进程对象
deviceInfo = readConf().get_device_info()  # 读取设备配置信息
deviceName = deviceInfo["deviceName"]  # 获取设备名称


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    在每个测试用例开始前启动 adb logcat，并清空设备日志。
    日志输出到 测试用例文件同级目录下 logs/device_logs/用例名.log 文件。
    同时设置pytest日志文件handler，输出到 logs/pytest_logs/用例名_pylog.log。
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
    pylog_file = os.path.join(pylog_dir, f"{item.name}_pylog.log")
   
    # 清空设备上的logcat日志
    subprocess.run(["adb", "-s", deviceName, "logcat", "-c"], check=True)
    # 启动 adb logcat，将日志写入文件（覆盖写入模式）
    log_process = subprocess.Popen(
        ["adb", "-s", deviceName, "logcat", "-v", "time"],
        stdout=open(log_file, "w"),  # 'w' 模式覆盖写入
        stderr=subprocess.STDOUT
    )
    logging.info(f"Started adb logcat for test case: {item.name}, log path: {log_file}")
    # 配置pytest日志文件handler（追加写入模式）
    logger = logging.getLogger()
    # 移除旧的文件handler，避免重复写入
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
    file_handler = logging.FileHandler(pylog_file, mode='a', encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    在每个测试用例结束后停止 adb logcat，并移除pytest日志文件handler。
    """
    global log_process
    logger = logging.getLogger()
    # 移除所有 FileHandler（只移除本次加的）
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
    
    if log_process:
        log_process.terminate()  # 终止adb logcat进程
        log_process.wait()       # 等待进程完全退出
        logging.info(f"Stopped adb logcat for test case: {item.name}")
        # 自动将logcat日志附加到allure报告
        case_dir = os.path.dirname(item.fspath)
        log_dir = os.path.join(case_dir, "logs", "device_logs")
        log_file = os.path.join(log_dir, f"{item.name}.log")
        if os.path.exists(log_file):
            with open(log_file, "rb") as f:
                allure.attach(f.read(), name=f"logcat_{item.name}", attachment_type=allure.attachment_type.TEXT)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 用于用例失败时自动截图并上传allure
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        # 获取driver对象
        driver = None
        if "app_init" in item.fixturenames:
            driver = item.funcargs["app_init"][0]
        if driver:
            try:
                png = driver.screenshot_as_png
                allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                logging.warning(f"截图失败: {e}")

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
    # 清除应用数据
    subprocess.run("adb -s {} shell pm clear {} ".format(deviceName, app_packageName), shell=True, check=True)


    # 返回设备对象、应用操作对象和配置对象
    yield (driver, app, r)

    # 测试完成后清理工作
    # 清除应用数据
    subprocess.run("adb -s {} shell pm clear {} ".format(deviceName, app_packageName), shell=True, check=True)
    # 停止应用
    app.stopApp()

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束后自动生成 Allure 报告。
    """
    import subprocess
    import shutil
    result_dir = os.path.abspath("allure-results")
    logging.info(f"Allure 结果目录: {result_dir}")

    report_dir = os.path.abspath("allure-report")
    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("未找到 allure 命令，请检查环境变量或手动生成报告。")
        return
    try:
        subprocess.run([
            allure_cmd, "generate", result_dir, "-o", report_dir, "--clean"
        ], check=True)
        print(f"Allure 报告已自动生成，路径: {report_dir}")
    except Exception as e:
        print(f"Allure 报告生成失败: {e}")
    # 自动在测试会话结束后打开 Allure 报告（仅限本地环境）
    try:
        os.system("allure open allure-report")
    except Exception as e:
        print(f"自动打开 Allure 报告失败: {e}")

