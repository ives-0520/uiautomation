import subprocess
import os

def open_allure_report():
    # Replace 'C:/path/to/allure' with the actual path to your allure executable
    allure_path = r'C:\allure-2.34.0\bin\allure.bat'
    cmd = [allure_path, 'open', 'report/allure-report']
    # 启动进程
    proc = subprocess.Popen(cmd)
    input("按回车键关闭Allure报告并销毁进程...")
    proc.terminate()

if __name__ == '__main__':
    open_allure_report()