"""基础页面类 - 所有页面对象的父类"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config


class BasePage:
    """基础页面类，提供通用的页面操作方法"""
    
    def __init__(self, driver):
        """初始化页面对象
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def find_element(self, locator):
        """查找单个元素
        
        Args:
            locator: 元素定位器 (By, value)
            
        Returns:
            WebElement: 找到的元素
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"无法找到元素: {locator}")
    
    def find_elements(self, locator):
        """查找多个元素
        
        Args:
            locator: 元素定位器 (By, value)
            
        Returns:
            list: 找到的元素列表
        """
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def click_element(self, locator):
        """点击元素
        
        Args:
            locator: 元素定位器 (By, value)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def input_text(self, locator, text):
        """输入文本
        
        Args:
            locator: 元素定位器 (By, value)
            text: 要输入的文本
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """获取元素文本
        
        Args:
            locator: 元素定位器 (By, value)
            
        Returns:
            str: 元素文本内容
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """检查元素是否可见
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 等待超时时间
            
        Returns:
            bool: 元素是否可见
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout=30):
        """等待页面加载完成
        
        Args:
            timeout: 等待超时时间
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def get_current_url(self):
        """获取当前页面URL
        
        Returns:
            str: 当前页面URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """获取页面标题
        
        Returns:
            str: 页面标题
        """
        return self.driver.title