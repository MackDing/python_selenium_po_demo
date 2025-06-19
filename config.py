"""配置文件 - 管理测试环境配置"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Config:
    """测试配置类"""
    
    # 测试网站URL
    BASE_URL = "https://www.saucedemo.com"
    
    # 测试用户信息
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    LOCKED_USERNAME = "locked_out_user"
    INVALID_USERNAME = "invalid_user"
    INVALID_PASSWORD = "invalid_password"
    
    # 浏览器配置
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    
    @staticmethod
    def get_driver():
        """获取WebDriver实例"""
        if Config.BROWSER.lower() == "chrome":
            chrome_options = Options()
            
            if Config.HEADLESS:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.maximize_window()
            
            return driver
        else:
            raise ValueError(f"不支持的浏览器类型: {Config.BROWSER}")