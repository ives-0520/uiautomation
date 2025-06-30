"""
元素操作模块
该模块定义了ElementOption类，提供了各种UI元素操作方法，如：
- 元素定位
- 点击操作
- 输入文本
- 获取屏幕尺寸
- 等待操作
等
"""

import ast
import inspect
from os import name
import time  # 用于延时操作
import logging  # 用于日志记录
from datetime import datetime  # 用于日期时间操作
from pathlib import Path  # 用于路径操作
from py import log
from selenium.webdriver.support.wait import WebDriverWait  # 用于显式等待
from selenium.webdriver.common.keys import Keys
from torch import device
import re  # 用于正则表达式匹配
import ai

class ElementOption():
    """
    元素操作类
    提供各种UI元素操作方法，如元素定位、点击、输入文本、等待等
    
    主要功能：
    1. 元素定位：查找单个或多个元素
    2. 输入操作：向输入框输入文本
    3. 点击操作：点击元素
    4. 屏幕操作：获取屏幕尺寸
    5. 等待操作：强制等待
    6. 键盘操作：回车键
    7. 元素判断：判断元素是否存在
    """

    def __init__(self, device):
        """
        初始化元素操作对象
        :param device: 设备对象，通常是uiautomator2的设备实例
        """
        self.device = device  # 设备对象


    def loadelement(self, element, retries=6, delay=1):
        """
        定位单个元素，带重试机制
        :param element: 元素定位信息，通常是一个字典，包含resourceId、text等定位信息，
                        或者是"(x,y)"格式的字符串
        :param retries: 重试次数，默认3次
        :param delay: 每次重试间隔秒数，默认0.5秒
        :return: 定位到的元素对象，如果未找到则返回None；
        """

        for attempt in range(retries):
            try:
                if isinstance(element, str) and '//' in element:
                    el_obj = self.device.xpath(element)
                else:
                    el_obj = self.device(**element)  # 使用传入的定位信息查找元素
                # el_obj = self.device(**element)  # 使用传入的定位信息查找元素
                # logging.info(f"Element loaded successfully: {el_obj.info}")
                return el_obj  # 返回找到的元素对象
            except Exception as e:
                logging.error(f"{element}Element load false (attempt {attempt+1}/{retries}): {e}")
                time.sleep(delay)
        return None

    def loadelements(self, element):
        """
        定位多个元素
        :param element: 元素的resourceId
        :return: 定位到的元素列表
        """
        els = self.device(resourceId=element)  # 使用resourceId查找多个元素
        return els

    def secondary_find_element(self, driver, element):
        """
        二级元素定位（在已找到的元素内查找子元素）
        :param driver: 驱动对象
        :param element: 元素定位信息
        :return: 定位到的子元素对象
        """
        second_el = driver.find_element(*element)  # 使用解包操作符传递定位信息
        return second_el

    def enter_(self, element, text):
        """
        向元素输入文本
        :param element: 元素定位信息
        :param text: 要输入的文本
        """
        
        if not isinstance(text, str):
            text = str(text)
        
        # 如果element是(x, y)格式且x、y都是数字，则直接点击坐标
        if (
            isinstance(element, (tuple, list)) and 
            len(element) == 2 and 
            all(isinstance(coord, (int, float)) for coord in element)
        ):
            
           
            x, y = element
            self.device.send_keys(text)
        else:
            self.loadelement(element).send_keys(text)  # 定位元素并输入文本


    def click_(self, element):
        """
        点击元素
        :param element: 元素定位信息或(x, y)坐标元组/列表
        """
        # 如果element是(x, y)格式且x、y都是数字，则直接点击坐标
        if (
            isinstance(element, (tuple, list)) and 
            len(element) == 2 and 
            all(isinstance(coord, (int, float)) for coord in element)
        ):
            
           
            x, y = element
            self.device.click(x, y)
            # logging.info(f"Clicking at coordinates: {element}")
        else:
            self.loadelement(element).click()
            

    def double_click(self, element):
        """
        双击元素
        :param element: 元素定位信息
        """
        el = self.loadelement(element)  # 定位元素
        if el:
            bounds = el.info['bounds']  # 获取元素的边界信息
            x = (bounds['left'] + bounds['right']) // 2  # 计算元素中心的x坐标
            y = (bounds['top'] + bounds['bottom']) // 2  # 计算元素中心的y坐标
            self.device.double_click(x, y)  # 使用uiautomator2的double_click方法双击元素

    def keys_down(self, times=1):
        """
        按遥控器下键多次
        :param times: 按下键的次数，默认为1
        """
        for _ in range(times):
            self.device.press("down")  # 模拟按遥控器下键
    
    def keys_up(self, times=1):
        """
        按遥控器上键多次
        :param times: 按上键的次数，默认为1
        """
        for _ in range(times):
            self.device.press("up")  # 模拟按遥控器上键

    def clear_input(self, element):
        """
        清空输入框内容
        :param element: 元素定位信息
        """
        el = self.loadelement(element)  # 定位元素
        if el:
            el.set_text('')  # 清空输入框内容


    def getSize(self):
        """
        获取屏幕尺寸
        :return: 包含屏幕宽高的字典，如{'width': 1080, 'height': 1920}
        """
        device_size = self.device.window_size()  # 获取设备窗口大小
        return device_size
       

    def wait(self, t):
        """
        强制等待
        :param t: 等待时间（秒）
        """
        self.device.wait(t)  # 设备等待指定时间



    def keys_enter(self, element):
        """
        向元素发送回车键
        :param element: 元素定位信息
        """
        
        self.loadelement(element).send_keys(Keys.ENTER)  # 定位元素并发送回车键

    def is_el_exists(self, element, retries=6, delay=1):
        """
        判断元素是否存在，增加重试机制
        :param element: 元素定位信息
        :param retries: 重试次数，默认6次
        :param delay: 每次重试间隔秒数，默认1秒
        :return: 元素存在返回True，不存在返回False
        """
        for attempt in range(retries):
            el = self.loadelement(element)
            if el is not None and el.exists:
                return True
            time.sleep(delay)
        return False
    
    def get_element_text(self, element):
        """
        获取元素的文本内容
        :param element: 元素定位信息
        :return: 元素的文本内容，如果未找到元素则返回None
        """
        el = self.loadelement(element)
        if el:
            return el.get_text() if hasattr(el, "get_text") else el.text
        return None
    



    
    

   

    def ai_loadelement(self, image_path, prompt, name='', version='1.0'):
        """
        仅用AI定位元素
        :param image_path: 当前页面截图路径
        :param prompt: AI定位描述
        :return: 定位到的元素对象，如果未找到则返回None
        """
        from ai.ai_tools import ImageAI
        import json
       
        locator = ImageAI()
        ai_result = locator.ai_locate(image_path, prompt)
        logging.info(f"AI定位返回结果: {ai_result}")
        ai_result_json = locator.format_ai_result(ai_result)
        
        ai_result_json=self.assemble_element_data(ai_result_json, name, version)


        # 保存AI返回结果到文件
        result_file = Path(image_path).with_suffix('.ai_result.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(ai_result_json, f, ensure_ascii=False, indent=2)
        logging.info(f"AI定位结果已保存到: {result_file}")
        
        

        ai_text=locator.extract_element_text(ai_result, prompt)
        ai_text = {"text":ai_text}  
        logging.info(f"AI定位元素文本: {ai_text}")
        # 提取相对坐标
        ai_coordinates = locator.extract_relative_coordinates(ai_result)
        if ai_coordinates is None:
            logging.error("AI定位未返回有效的相对坐标")
            return None
        
        logging.info(f"AI定位元素相对坐标: {ai_coordinates}")


        # element_info= self.loadelement(ai_text).info
        # logging.info(f"AI定位元素信息: {element_info}")
     

      
        # 始终以元组的方式输出
        if not isinstance(ai_coordinates, tuple):
            return ast.literal_eval(ai_coordinates)
        

        return ai_coordinates

    def hybrid_loadelement(self, element_option):
        """
        传统+AI混合定位，优先传统，失败时AI兜底（api_key已在ImageLocator内部写死）
        :param element: 传统元素定位信息
        :return: 定位到的元素对象，如果未找到则返回None
        """
        element = element_option.locator
        name = element_option.name
        version = element_option.find_version 
        if isinstance(element, (list)):
            # logging.warning("传入的元素是list类型，转换为元组")
            return tuple(element)

        el = self.loadelement(element)
        if el and el.exists:
            return element
        
        logging.info("元素" + str(element) + "传统定位失败，尝试AI定位...")
        # 自动截图
        # 获取调用该方法的pytest测试用例文件的同级目录
        # 查找调用栈中第一个pytest测试用例文件（以test_开头或结尾为_test.py）
        for frame_info in inspect.stack():
            filename = frame_info.filename
            if (filename.endswith('.py') and 
            (Path(filename).name.startswith('test_') or Path(filename).name.endswith('_test.py'))):
                case_dir = Path(filename).parent
                break
        else:
            # 如果未找到，退回当前文件目录
            case_dir = Path(__file__).parent
        images_dir = case_dir / "images"
        images_dir.mkdir(exist_ok=True)
        image_path = images_dir / f"ai_fallback_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.device.screenshot(str(image_path))
        
        logging.info(f"截图已保存，图片地址: {image_path}")
        # 用element作为prompt
        prompt = str(element)
        return self.ai_loadelement(image_path, prompt,name, version)
    
    def assemble_element_data(self,ai_data, name, version):
        """
        组装元素数据为指定格式
        :param ai_data: AI元素数据字典，格式如{"ai": {...}}
        :param name: 元素名称字符串
        :param version: 版本号字符串
        :return: 组装后的字典
        """
        return {
            name: {
                version: ai_data
            }
        }

