import subprocess
import os
import signal
import logging

def run_weditor():
    # 杀死已存在的 weditor 进程
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/IM', 'weditor.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['pkill', '-f', 'weditor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"尝试杀死 weditor 进程时出错: {e}")
        logging.error(f"尝试杀死 weditor 进程时出错: {e}")

    # 启动新的 weditor 进程
    try:
        subprocess.run(['weditor'], check=True)
    except FileNotFoundError:
        print("weditor 未安装，请先通过 'pip install weditor' 安装。")
        logging.error("weditor 未安装，请先通过 'pip install weditor' 安装。")
    except subprocess.CalledProcessError as e:
        print(f"weditor 执行失败: {e}")
        logging.error(f"weditor 执行失败: {e}")

if __name__ == "__main__":
    run_weditor()