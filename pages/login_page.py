"""登录页面对象类"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class LoginPage(BasePage):
    """登录页面类，继承自BasePage"""
    
    # 页面元素定位器
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, "[data-test='error-button']")
    
    def __init__(self, driver):
        """初始化登录页面
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    
    def open(self, url):
        """打开登录页面
        
        Args:
            url: 登录页面URL
        """
        self.driver.get(url)
        self.wait_for_page_load()
    
    def enter_username(self, username):
        """输入用户名
        
        Args:
            username: 用户名
        """
        self.input_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """输入密码
        
        Args:
            password: 密码
        """
        self.input_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self):
        """获取错误信息
        
        Returns:
            str: 错误信息文本
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self):
        """检查是否显示错误信息
        
        Returns:
            bool: 是否显示错误信息
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def close_error_message(self):
        """关闭错误信息"""
        if self.is_element_visible(self.ERROR_BUTTON):
            self.click_element(self.ERROR_BUTTON)
    
    def is_login_page(self):
        """检查是否在登录页面
        
        Returns:
            bool: 是否在登录页面
        """
        return self.is_element_visible(self.LOGIN_BUTTON) and \
               self.is_element_visible(self.USERNAME_INPUT) and \
               self.is_element_visible(self.PASSWORD_INPUT)
    
    def clear_username(self):
        """清空用户名输入框"""
        element = self.find_element(self.USERNAME_INPUT)
        element.clear()
    
    def clear_password(self):
        """清空密码输入框"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.clear()
    
    def get_username_value(self):
        """获取用户名输入框的值
        
        Returns:
            str: 用户名输入框的值
        """
        element = self.find_element(self.USERNAME_INPUT)
        return element.get_attribute("value")
    
    def get_password_value(self):
        """获取密码输入框的值
        
        Returns:
            str: 密码输入框的值
        """
        element = self.find_element(self.PASSWORD_INPUT)
        return element.get_attribute("value")