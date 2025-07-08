"""
测试夹具模块  # Test fixture module
该模块定义了各种pytest夹具(fixtures)，用于测试前的准备工作和测试后的清理工作。  # This module defines various pytest fixtures for setup and teardown.
包括应用初始化、设备连接、数据准备等功能。  # Includes app initialization, device connection, data preparation, etc.
"""

import datetime
from numpy import info
from py import log
import pytest  # 用于测试框架  # For test framework
import subprocess  # 用于执行系统命令  # For executing system commands
from device.adbOperation import ADBOperation  # 导入ADB操作类  # Import ADB operation class
from config.read_config import readConf  # 导入配置读取类  # Import config reader class
from device import device_init  # 导入设备初始化模块  # Import device initialization module
import os  # 用于文件和目录操作  # For file and directory operations
import logging
import allure  # 导入allure
import json  # 新增
import glob  # 新增
import sys
from ai.ai_tools import LanguageAI  # 导入AI工具类

log_process = None  # 全局变量，用于保存adb logcat子进程对象  # Global variable for adb logcat process
deviceInfo = readConf().get_device_info()  # 读取设备配置信息
deviceName = deviceInfo["deviceName"]  # 获取设备名称

def update_element_locators_with_ai_result(item=None):
    """
    检查当前用例目录下是否有ai_result.json类文件，若有则合并到element_locators.json。  # Check if ai_result.json exists and merge to element_locators.json
    用于自动将AI识别的元素定位信息合并到主元素库，便于后续用例复用。  # Automatically merge AI element locators for reuse
    """
    # 获取当前测试用例文件所在目录（如果item传入则用item.fspath，否则用conftest.py目录）  # Get test case directory
    if item is not None and hasattr(item, 'fspath'):
        case_dir = os.path.dirname(item.fspath)
    else:
        case_dir = os.path.dirname(__file__)
    # 修正：主元素库json路径，向上三级到APP_UI_AUTO根目录再拼接element_manage/element_locators.json  # Main element locator path
    element_locators_path = os.path.abspath(os.path.join(case_dir, '../../../element_manage/element_locators.json'))
    # 查找images目录下所有ai_fallback_*.ai_result.json文件（AI识别结果文件）  # Find all AI result files in images dir
    ai_result_files = glob.glob(os.path.join(case_dir, 'images', 'ai_fallback_*.ai_result.json'))
    if not ai_result_files:
        # 如果没有AI识别结果文件，直接返回  # Return if no AI result files
        return
    # 读取主元素库文件  # Read main element locator file
    with open(element_locators_path, 'r', encoding='utf-8') as f:
        element_locators = json.load(f)
    updated = False  # 标记是否有更新  # Flag for update
    # 遍历所有AI识别结果文件  # Iterate all AI result files
    for ai_file in ai_result_files:
        with open(ai_file, 'r', encoding='utf-8') as f:
            ai_data = json.load(f)
        # 遍历AI识别结果中的每个元素
        for elem_key, elem_val in ai_data.items():
            for version, version_val in elem_val.items():
                # 如果主元素库中没有该元素，则新建  # Create if element not in main locator
                if elem_key not in element_locators:
                    element_locators[elem_key] = {}
                # 如果主元素库中没有该版本，则新建  # Create if version not in main locator
                if version not in element_locators[elem_key]:
                    element_locators[elem_key][version] = {}
                # 如果AI识别结果中有'ai'字段，则合并到主元素库  # Merge 'ai' field if exists
                if 'ai' in version_val:
                    element_locators[elem_key][version]['ai'] = version_val['ai']
                    updated = True
    # 如果有更新，则写回主元素库文件  # Write back if updated
    if updated:
        with open(element_locators_path, 'w', encoding='utf-8') as f:
            json.dump(element_locators, f, ensure_ascii=False, indent=4)
        logging.info(f"已自动合并AI识别元素到主元素库: {element_locators_path}")  # Auto-merged AI elements to main locator



@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    在每个测试用例开始前启动 adb logcat，并清空设备日志。  # Start adb logcat and clear logs before each test
    日志输出到 测试用例文件同级目录下 logs/device_logs/用例名.log 文件。  # Log output to logs/device_logs/case_name.log
    同时设置pytest日志文件handler，输出到 logs/pytest_logs/用例名_pylog.log。  # Pytest log output to logs/pytest_logs/case_name_pylog.log
    """
    global log_process
    
    # 获取当前测试用例文件的目录  # Get test case file directory
    case_dir = os.path.dirname(item.fspath)
    # 构造 logs/device_logs 目录  # Create logs/device_logs dir
    log_dir = os.path.join(case_dir, "logs", "device_logs")
    os.makedirs(log_dir, exist_ok=True)
    # 构造 logs/pytest_logs 目录  # Create logs/pytest_logs dir
    pylog_dir = os.path.join(case_dir, "logs", "pytest_logs")
    os.makedirs(pylog_dir, exist_ok=True)
    # 日志文件路径  # Log file path
    log_file = os.path.join(log_dir, f"{item.name}.log")
    pylog_file = os.path.join(pylog_dir, f"{item.name}_pylog.log")

    # 配置pytest日志文件handler  # Configure pytest log file handler
    logger = logging.getLogger()
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
    file_handler = logging.FileHandler(pylog_file, mode='w', encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
   
    # 清空设备上的logcat日志  # Clear device logcat logs
    subprocess.run(["adb", "-s", deviceName, "logcat", "-c"], check=True)
    # 启动 adb logcat，将日志写入文件（覆盖写入模式）  # Start adb logcat, write logs to file
    log_process = subprocess.Popen(
        ["adb", "-s", deviceName, "logcat", "-v", "time"],
        stdout=open(log_file, "w"),  # 'w' 模式覆盖写入
        stderr=subprocess.STDOUT
    )
    logging.info(f"Started adb logcat for test case: {item.name}, log path: {log_file}")  # Log start
    
    

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    在每个测试用例结束后停止 adb logcat，并移除pytest日志文件handler。  # Stop adb logcat and remove pytest log handler after each test
    """
    global log_process
    
    
    if log_process:
        log_process.terminate()  # 终止adb logcat进程  # Terminate adb logcat process
        log_process.wait()       # 等待进程完全退出  # Wait for process to exit
        logging.info(f"Stopped adb logcat for test case: {item.name}")  # Log stop
        # 自动将logcat日志附加到allure报告  # Attach logcat log to allure report
        case_dir = os.path.dirname(item.fspath)
        log_dir = os.path.join(case_dir, "logs", "device_logs")
        log_file = os.path.join(log_dir, f"{item.name}.log")
        if os.path.exists(log_file):
            with open(log_file, "rb") as f:
                allure.attach(f.read(), name=f"logcat_{item.name}", attachment_type=allure.attachment_type.TEXT)
    
    logger = logging.getLogger()
    # 移除所有 FileHandler  # Remove all FileHandlers
    for h in logger.handlers[:]:
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
   
    outcome = yield
    rep = outcome.get_result()
    # 用例成功后自动合并ai_result到element_locators  # Auto-merge ai_result to element_locators on success
    if rep.when == "call" and rep.passed:
        info = f"用例 {item.name} 执行成功"  # Test case executed successfully
        logging.info(info) 

        try:
            update_element_locators_with_ai_result(item)
        except Exception as e:
            logging.warning(f"自动合并AI定位信息失败: {e}")  # Auto-merge AI locator failed


    # 用于用例失败时自动截图并上传allure  # Auto screenshot and upload to allure on failure
    if rep.when == "call" and rep.failed:
        info = f"用例 {item.name} 执行失败"  # Test case failed
        logging.error(info)

        error_info = {
            "error_type": str(call.excinfo.type),  # 异常类型  # Exception type
            "error_message": str(call.excinfo.value),  # 错误信息  # Error message
            "error_traceback": str(call.excinfo.getrepr()),  # 错误回溯信息  # Error traceback
        }
        # logging.error(f"用例 {item.name} 错误信息: {error_info}")  # Log error info
        # 写入到测试用例对应的pytest日志文件  # Write to pytest log file
        case_dir = os.path.dirname(item.fspath)
        pylog_dir = os.path.join(case_dir, "logs", "pytest_logs")
        pylog_file = os.path.join(pylog_dir, f"{item.name}_pylog.log")
        # with open(pylog_file, "a", encoding="utf-8") as f:
        #     f.write("\n[ERROR_INFO]\n")
        #     f.write(json.dumps(error_info, ensure_ascii=False, indent=4))
        #     f.write("\n")



        # analyze_log_and_suggest_result = LanguageAI().analyze_log_and_suggest(pylog_file)
        # if analyze_log_and_suggest_result:
        #     logging.info(f"AI日志分析建议: {analyze_log_and_suggest_result}")  # Log AI suggestion
        #     allure.attach(
        #     analyze_log_and_suggest_result,
        #     name=f"AI日志分析建议_{item.name}",
        #     attachment_type=allure.attachment_type.TEXT
        #     )
       

        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
                tmp_path = tmpfile.name
            adb_path = f"/sdcard/pytest_fail_{item.name}.png"
            # 截图到设备  # Screenshot to device
            subprocess.run(["adb", "-s", deviceName, "shell", "screencap", "-p", adb_path], check=True)
            # 拉取到本地  # Pull to local
            subprocess.run(["adb", "-s", deviceName, "pull", adb_path, tmp_path], check=True)
            # 删除设备上的截图  # Delete screenshot on device
            subprocess.run(["adb", "-s", deviceName, "shell", "rm", adb_path], check=True)
            if os.path.exists(tmp_path):
                with open(tmp_path, 'rb') as f:
                    allure.attach(f.read(), name=f"用例执行失败截图_{item.name}", attachment_type=allure.attachment_type.PNG)  # Attach failure screenshot
                os.remove(tmp_path)
            else:
                logging.warning("adb截图失败: 未生成图片")  # adb screenshot failed: no image
        except Exception as e:
            logging.warning(f"adb截图失败: {e}")  # adb screenshot failed
        

@pytest.fixture
def app_init():
    """
    测试用例初始化夹具。  # Test case initialization fixture
    连接设备，初始化应用对象，测试结束后清理应用数据并关闭应用。  # Connect device, initialize app, cleanup after test
    返回(driver, app, 配置对象)元组。  # Return (driver, app, config)
    """
    global deviceName
    r = readConf()  # 创建配置读取对象  # Create config reader
    adb = ADBOperation()  # 创建ADB操作对象  # Create ADB operation object
    adb.connect_device(deviceName)  # 连接设备  # Connect device
    global u2_driver
    driver = device_init.d  # 获取设备对象  # Get device object
    u2_driver = driver      # 赋值全局driver  # Assign global driver
    # 新增：初始化manager  # New: initialize manager
    from element_manage.element_locator_manager import ElementLocatorManager
    locator_path = os.path.join(os.path.dirname(__file__), '../../element_manage/element_locators.json')
    packageName = device_init.packageName
    manager = ElementLocatorManager(locator_path, packageName, 'v2')
    app = device_init.appOpt(driver, manager)  # 创建应用操作对象  # Create app operation object
    deviceName = device_init.deviceName  # 获取设备名称  # Get device name
    app_packageName = device_init.packageName  # 获取应用包名  # Get app package name
    # 清除应用数据  # Clear app data
    subprocess.run("adb -s {} shell pm clear {} ".format(deviceName, app_packageName), shell=True, check=True)


    # 返回设备对象、应用操作对象和配置对象  # Return device, app, config, manager
    yield (driver, app, r,manager)

    # 测试完成后清理工作  # Cleanup after test
    # 清除应用数据  # Clear app data
    subprocess.run("adb -s {} shell pm clear {} ".format(deviceName, app_packageName), shell=True, check=True)
    # 停止应用  # Stop app
    app.stopApp()

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束后自动生成 Allure 报告。  # Auto-generate Allure report after test session
    """
    import subprocess
    import shutil


    result_dir = os.path.abspath("report/allure-results")
    logging.info(f"Allure 结果目录: {result_dir}")  # Allure result directory

    report_dir = os.path.abspath("report/allure-report")
    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("未找到 allure 命令，请检查环境变量或手动生成报告。")  # Allure command not found
        return
    try:
        subprocess.run([
            allure_cmd, "generate", result_dir, "-o", report_dir, "--clean"
        ], check=True)
        print(f"Allure 报告已自动生成，路径: {report_dir}")  # Allure report generated
    except Exception as e:
        print(f"Allure 报告生成失败: {e}")  # Allure report generation failed
    # 自动在测试会话结束后打开 Allure 报告（仅限本地环境）  # Auto open Allure report (local only)
    # try:
    #     os.system("allure open report\allure-report")
    # except Exception as e:
    #     print(f"自动打开 Allure 报告失败: {e}")

