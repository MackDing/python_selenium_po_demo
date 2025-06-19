"""产品页面对象类"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductsPage(BasePage):
    """产品页面类，继承自BasePage"""
    
    # 页面元素定位器
    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_ICON = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    
    # 产品相关元素
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "[data-test^='remove']")
    
    # 具体产品的添加到购物车按钮
    ADD_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BIKE_LIGHT_BUTTON = (By.ID, "add-to-cart-sauce-labs-bike-light")
    ADD_BOLT_TSHIRT_BUTTON = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    
    def __init__(self, driver):
        """初始化产品页面
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
    
    def is_products_page(self):
        """检查是否在产品页面
        
        Returns:
            bool: 是否在产品页面
        """
        return self.is_element_visible(self.PAGE_TITLE) and \
               "Products" in self.get_page_title_text()
    
    def get_page_title_text(self):
        """获取页面标题文本
        
        Returns:
            str: 页面标题文本
        """
        if self.is_element_visible(self.PAGE_TITLE):
            return self.get_text(self.PAGE_TITLE)
        return ""
    
    def click_menu_button(self):
        """点击菜单按钮"""
        self.click_element(self.MENU_BUTTON)
    
    def logout(self):
        """执行登出操作"""
        self.click_menu_button()
        # 等待菜单展开
        self.wait.until(lambda driver: self.is_element_visible(self.LOGOUT_LINK))
        self.click_element(self.LOGOUT_LINK)
    
    def click_cart_icon(self):
        """点击购物车图标"""
        self.click_element(self.CART_ICON)
    
    def get_cart_items_count(self):
        """获取购物车中商品数量
        
        Returns:
            int: 购物车中商品数量
        """
        if self.is_element_visible(self.CART_BADGE):
            count_text = self.get_text(self.CART_BADGE)
            return int(count_text) if count_text.isdigit() else 0
        return 0
    
    def get_product_names(self):
        """获取所有产品名称
        
        Returns:
            list: 产品名称列表
        """
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in elements]
    
    def get_product_prices(self):
        """获取所有产品价格
        
        Returns:
            list: 产品价格列表
        """
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [element.text for element in elements]
    
    def get_products_count(self):
        """获取产品总数
        
        Returns:
            int: 产品总数
        """
        products = self.find_elements(self.PRODUCT_ITEMS)
        return len(products)
    
    def add_product_to_cart_by_name(self, product_name):
        """根据产品名称添加产品到购物车
        
        Args:
            product_name: 产品名称
        """
        # 构建动态定位器
        product_id = product_name.lower().replace(" ", "-")
        add_button_locator = (By.ID, f"add-to-cart-{product_id}")
        self.click_element(add_button_locator)
    
    def add_backpack_to_cart(self):
        """添加背包到购物车"""
        self.click_element(self.ADD_BACKPACK_BUTTON)
    
    def add_bike_light_to_cart(self):
        """添加自行车灯到购物车"""
        self.click_element(self.ADD_BIKE_LIGHT_BUTTON)
    
    def add_bolt_tshirt_to_cart(self):
        """添加T恤到购物车"""
        self.click_element(self.ADD_BOLT_TSHIRT_BUTTON)
    
    def remove_product_from_cart_by_name(self, product_name):
        """根据产品名称从购物车移除产品
        
        Args:
            product_name: 产品名称
        """
        # 构建动态定位器
        product_id = product_name.lower().replace(" ", "-")
        remove_button_locator = (By.ID, f"remove-{product_id}")
        self.click_element(remove_button_locator)
    
    def is_product_added_to_cart(self, product_name):
        """检查产品是否已添加到购物车
        
        Args:
            product_name: 产品名称
            
        Returns:
            bool: 产品是否已添加到购物车
        """
        product_id = product_name.lower().replace(" ", "-")
        remove_button_locator = (By.ID, f"remove-{product_id}")
        return self.is_element_visible(remove_button_locator, timeout=2)
    
    def select_sort_option(self, option_value):
        """选择排序选项
        
        Args:
            option_value: 排序选项值 (za, az, lohi, hilo)
        """
        from selenium.webdriver.support.ui import Select
        dropdown_element = self.find_element(self.SORT_DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_value(option_value)