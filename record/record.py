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
            # 检查 pkill 是否可用
            if subprocess.run(['which', 'pkill'], stdout=subprocess.DEVNULL).returncode == 0:
                subprocess.run(['pkill', '-f', 'weditor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print("未找到 pkill 命令，请手动关闭 weditor 进程。")
                logging.warning("未找到 pkill 命令，请手动关闭 weditor 进程。")
    except Exception as e:
        print(f"尝试杀死 weditor 进程时出错: {e}")
        logging.error(f"尝试杀死 weditor 进程时出错: {e}")

    # 启动新的 weditor 进程
    try:
        proc = subprocess.Popen(['weditor'])
        input("按回车键销毁 weditor 进程并退出...")
        # 用户按下回车后销毁进程
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/PID', str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.terminate()
        
    except FileNotFoundError:
        print("weditor 未安装，请先通过 'pip install weditor' 安装。")
        logging.error("weditor 未安装，请先通过 'pip install weditor' 安装。")
    except subprocess.CalledProcessError as e:
        print(f"weditor 执行失败: {e}")
        logging.error(f"weditor 执行失败: {e}")

if __name__ == "__main__":
    run_weditor()