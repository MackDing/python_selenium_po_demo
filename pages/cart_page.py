"""购物车页面对象类"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class CartPage(BasePage):
    """购物车页面类，继承自BasePage"""
    
    # 页面元素定位器
    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    
    # 购物车商品相关元素
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    CART_ITEM_QUANTITIES = (By.CSS_SELECTOR, "[data-test='item-quantity']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "[data-test^='remove']")
    
    # 空购物车元素
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart_list")
    
    def __init__(self, driver):
        """初始化购物车页面
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    
    def is_cart_page(self):
        """检查是否在购物车页面
        
        Returns:
            bool: 是否在购物车页面
        """
        return self.is_element_visible(self.PAGE_TITLE) and \
               "Your Cart" in self.get_page_title_text()
    
    def get_page_title_text(self):
        """获取页面标题文本
        
        Returns:
            str: 页面标题文本
        """
        if self.is_element_visible(self.PAGE_TITLE):
            return self.get_text(self.PAGE_TITLE)
        return ""
    
    def click_continue_shopping(self):
        """点击继续购物按钮"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_checkout(self):
        """点击结账按钮"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def get_cart_items_count(self):
        """获取购物车中商品数量
        
        Returns:
            int: 购物车中商品数量
        """
        items = self.find_elements(self.CART_ITEMS)
        return len(items)
    
    def get_cart_item_names(self):
        """获取购物车中所有商品名称
        
        Returns:
            list: 商品名称列表
        """
        elements = self.find_elements(self.CART_ITEM_NAMES)
        return [element.text for element in elements]
    
    def get_cart_item_prices(self):
        """获取购物车中所有商品价格
        
        Returns:
            list: 商品价格列表
        """
        elements = self.find_elements(self.CART_ITEM_PRICES)
        return [element.text for element in elements]
    
    def get_cart_item_quantities(self):
        """获取购物车中所有商品数量
        
        Returns:
            list: 商品数量列表
        """
        elements = self.find_elements(self.CART_ITEM_QUANTITIES)
        return [int(element.text) for element in elements if element.text.isdigit()]
    
    def remove_item_by_name(self, product_name):
        """根据商品名称移除商品
        
        Args:
            product_name: 商品名称
        """
        # 构建动态定位器
        product_id = product_name.lower().replace(" ", "-")
        remove_button_locator = (By.ID, f"remove-{product_id}")
        self.click_element(remove_button_locator)
    
    def is_item_in_cart(self, product_name):
        """检查商品是否在购物车中
        
        Args:
            product_name: 商品名称
            
        Returns:
            bool: 商品是否在购物车中
        """
        item_names = self.get_cart_item_names()
        return product_name in item_names
    
    def is_cart_empty(self):
        """检查购物车是否为空
        
        Returns:
            bool: 购物车是否为空
        """
        return self.get_cart_items_count() == 0
    
    def clear_cart(self):
        """清空购物车"""
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS)
        for button in remove_buttons:
            button.click()
    
    def get_total_price(self):
        """计算购物车总价格
        
        Returns:
            float: 总价格
        """
        prices = self.get_cart_item_prices()
        total = 0.0
        for price_text in prices:
            # 移除货币符号并转换为浮点数
            price = float(price_text.replace('$', ''))
            total += price
        return total
    
    def is_checkout_button_enabled(self):
        """检查结账按钮是否可用
        
        Returns:
            bool: 结账按钮是否可用
        """
        if self.is_element_visible(self.CHECKOUT_BUTTON):
            button = self.find_element(self.CHECKOUT_BUTTON)
            return button.is_enabled()
        return False
    
    def is_continue_shopping_button_visible(self):
        """检查继续购物按钮是否可见
        
        Returns:
            bool: 继续购物按钮是否可见
        """
        return self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON)