"""pytest配置文件 - 提供测试夹具和配置"""

import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pages import LoginPage, ProductsPage, CartPage


@pytest.fixture(scope="function")
def driver():
    """
    定义一个名为 'driver' 的 fixture。
    scope="function" 表示每个测试函数都会执行一次这个fixture，
    确保测试之间的独立性。
    """
    print("\n[Pytest Fixture] 启动浏览器...")
    
    # --- 开始修改 ---
    
    # 1. 创建 ChromeOptions 对象
    chrome_options = Options()
    
    # 2. 创建一个字典，用于存储实验性选项的偏好设置
    prefs = {
        "credentials_enable_service": False,  # 禁用凭据服务，这是关键
        "profile.password_manager_enabled": False  # 禁用密码管理器
    }
    
    # 3. 将偏好设置添加到 ChromeOptions 中
    chrome_options.add_experimental_option("prefs", prefs)
    
    # 4. (可选) 禁用 "Chrome正受到自动测试软件的控制" 的信息栏
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # 5. 添加其他有用的选项
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 6. 检查是否需要无头模式
    if os.getenv('HEADLESS', 'false').lower() == 'true':
        chrome_options.add_argument("--headless")
    
    # --- 修改结束 ---

    # 7. 在创建WebDriver实例时，传入配置好的 options
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(5)  # 设置隐式等待

    # 'yield' 关键字是fixture的核心，它将driver对象提供给测试函数
    yield browser

    # --- 后置操作 ---
    print("\n[Pytest Fixture] 关闭浏览器...")
    browser.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """登录页面夹具
    
    Args:
        driver: WebDriver实例
        
    Returns:
        LoginPage: 登录页面对象
    """
    page = LoginPage(driver)
    page.open(Config.BASE_URL)
    return page


@pytest.fixture(scope="function")
def products_page(driver):
    """产品页面夹具
    
    Args:
        driver: WebDriver实例
        
    Returns:
        ProductsPage: 产品页面对象
    """
    return ProductsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """购物车页面夹具
    
    Args:
        driver: WebDriver实例
        
    Returns:
        CartPage: 购物车页面对象
    """
    return CartPage(driver)


@pytest.fixture(scope="function")
def logged_in_user(login_page, products_page):
    """已登录用户夹具 - 自动登录标准用户
    
    Args:
        login_page: 登录页面对象
        products_page: 产品页面对象
        
    Returns:
        ProductsPage: 登录后的产品页面对象
    """
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
    assert products_page.is_products_page(), "登录失败，未跳转到产品页面"
    return products_page


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """测试环境设置夹具 - 在所有测试开始前执行"""
    # 创建测试报告目录
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    print("\n=== 测试环境设置完成 ===")
    print(f"测试网站: {Config.BASE_URL}")
    print(f"浏览器: {Config.BROWSER}")
    print(f"无头模式: {Config.HEADLESS}")
    print(f"报告目录: {reports_dir}")
    print("=" * 50)


@pytest.fixture(scope="function")
def test_data():
    """测试数据夹具
    
    Returns:
        dict: 测试数据字典
    """
    return {
        "valid_users": {
            "standard_user": {
                "username": Config.VALID_USERNAME,
                "password": Config.VALID_PASSWORD
            }
        },
        "invalid_users": {
            "locked_user": {
                "username": Config.LOCKED_USERNAME,
                "password": Config.VALID_PASSWORD
            },
            "invalid_user": {
                "username": Config.INVALID_USERNAME,
                "password": Config.INVALID_PASSWORD
            }
        },
        "products": {
            "backpack": "Sauce Labs Backpack",
            "bike_light": "Sauce Labs Bike Light",
            "bolt_tshirt": "Sauce Labs Bolt T-Shirt"
        }
    }


def pytest_configure(config):
    """pytest配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "smoke: 标记冒烟测试用例"
    )
    config.addinivalue_line(
        "markers", "regression: 标记回归测试用例"
    )
    config.addinivalue_line(
        "markers", "login: 标记登录相关测试用例"
    )
    config.addinivalue_line(
        "markers", "cart: 标记购物车相关测试用例"
    )


def pytest_runtest_makereport(item, call):
    """测试报告生成钩子"""
    if call.when == "call":
        # 可以在这里添加截图等功能
        pass