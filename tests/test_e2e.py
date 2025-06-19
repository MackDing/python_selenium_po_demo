"""端到端测试用例 - 测试完整的用户流程"""

import pytest
from config import Config


class TestEndToEnd:
    """端到端测试类"""
    
    @pytest.mark.smoke
    def test_complete_shopping_flow(self, login_page, products_page, cart_page):
        """测试完整的购物流程"""
        # 步骤1: 登录
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        assert products_page.is_products_page(), "登录后应该跳转到产品页面"
        
        # 步骤2: 浏览产品
        products_count = products_page.get_products_count()
        assert products_count > 0, "应该显示产品列表"
        
        product_names = products_page.get_product_names()
        product_prices = products_page.get_product_prices()
        assert len(product_names) == len(product_prices), "产品名称和价格数量应该一致"
        
        # 步骤3: 添加多个产品到购物车
        products_page.add_backpack_to_cart()
        products_page.add_bike_light_to_cart()
        assert products_page.get_cart_items_count() == 2, "购物车应该有2个商品"
        
        # 步骤4: 查看购物车
        products_page.click_cart_icon()
        assert cart_page.is_cart_page(), "应该跳转到购物车页面"
        
        # 验证购物车内容
        cart_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_items, "背包应该在购物车中"
        assert "Sauce Labs Bike Light" in cart_items, "自行车灯应该在购物车中"
        assert cart_page.get_cart_items_count() == 2, "购物车应该有2个商品"
        
        # 步骤5: 修改购物车（移除一个商品）
        cart_page.remove_item_by_name("Sauce Labs Backpack")
        assert cart_page.get_cart_items_count() == 1, "购物车应该还有1个商品"
        assert not cart_page.is_item_in_cart("Sauce Labs Backpack"), "背包应该已移除"
        
        # 步骤6: 继续购物
        cart_page.click_continue_shopping()
        assert products_page.is_products_page(), "应该返回到产品页面"
        assert products_page.get_cart_items_count() == 1, "购物车状态应该保持"
        
        # 步骤7: 添加更多商品
        products_page.add_bolt_tshirt_to_cart()
        assert products_page.get_cart_items_count() == 2, "购物车应该有2个商品"
        
        # 步骤8: 最终检查购物车
        products_page.click_cart_icon()
        final_items = cart_page.get_cart_item_names()
        assert "Sauce Labs Bike Light" in final_items, "自行车灯应该在最终购物车中"
        assert "Sauce Labs Bolt T-Shirt" in final_items, "T恤应该在最终购物车中"
        assert len(final_items) == 2, "最终购物车应该有2个商品"
        
        # 步骤9: 登出
        products_page.logout()
        assert login_page.is_login_page(), "登出后应该返回登录页面"
    
    @pytest.mark.regression
    def test_user_session_management(self, login_page, products_page):
        """测试用户会话管理"""
        # 登录
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        assert products_page.is_products_page(), "应该成功登录"
        
        # 添加商品到购物车
        products_page.add_backpack_to_cart()
        assert products_page.get_cart_items_count() == 1, "购物车应该有1个商品"
        
        # 登出
        products_page.logout()
        assert login_page.is_login_page(), "应该成功登出"
        
        # 尝试直接访问产品页面（应该被重定向到登录页面）
        login_page.driver.get(Config.BASE_URL + "/inventory.html")
        assert login_page.is_login_page(), "未登录用户应该被重定向到登录页面"
        
        # 重新登录
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        assert products_page.is_products_page(), "应该能够重新登录"
        
        # 验证购物车状态（通常会被清空，但这取决于应用的实现）
        cart_count = products_page.get_cart_items_count()
        # 注意：这里的断言取决于应用是否保持购物车状态
        print(f"重新登录后购物车商品数量: {cart_count}")
    
    @pytest.mark.regression
    def test_product_sorting_and_selection(self, logged_in_user, cart_page):
        """测试产品排序和选择流程"""
        # 获取默认产品列表
        default_products = logged_in_user.get_product_names()
        default_prices = logged_in_user.get_product_prices()
        
        # 按价格从低到高排序
        logged_in_user.select_sort_option("lohi")
        sorted_prices = logged_in_user.get_product_prices()
        
        # 验证排序效果
        price_values = [float(price.replace('$', '')) for price in sorted_prices]
        assert price_values == sorted(price_values), "价格应该按从低到高排序"
        
        # 选择最便宜的产品
        cheapest_price = min(price_values)
        cheapest_index = price_values.index(cheapest_price)
        sorted_products = logged_in_user.get_product_names()
        cheapest_product = sorted_products[cheapest_index]
        
        # 添加最便宜的产品到购物车
        # 这里需要根据产品名称构建对应的添加方法
        if "Backpack" in cheapest_product:
            logged_in_user.add_backpack_to_cart()
        elif "Bike Light" in cheapest_product:
            logged_in_user.add_bike_light_to_cart()
        elif "T-Shirt" in cheapest_product:
            logged_in_user.add_bolt_tshirt_to_cart()
        
        # 验证添加成功
        assert logged_in_user.get_cart_items_count() == 1, "应该添加了1个商品"
        
        # 查看购物车
        logged_in_user.click_cart_icon()
        cart_items = cart_page.get_cart_item_names()
        assert cheapest_product in cart_items, f"最便宜的产品'{cheapest_product}'应该在购物车中"
        
        # 验证价格
        cart_prices = cart_page.get_cart_item_prices()
        assert len(cart_prices) == 1, "购物车应该有1个商品的价格"
        cart_price_value = float(cart_prices[0].replace('$', ''))
        assert cart_price_value == cheapest_price, "购物车中的价格应该是最便宜的价格"
    
    @pytest.mark.smoke
    def test_error_handling_flow(self, login_page, products_page):
        """测试错误处理流程"""
        # 测试登录错误处理
        login_page.login("invalid_user", "invalid_pass")
        assert login_page.is_error_displayed(), "应该显示登录错误"
        
        error_message = login_page.get_error_message()
        assert "do not match" in error_message.lower(), "应该显示用户名密码不匹配错误"
        
        # 关闭错误信息
        login_page.close_error_message()
        assert not login_page.is_error_displayed(), "错误信息应该被关闭"
        
        # 测试锁定用户
        login_page.login(Config.LOCKED_USERNAME, Config.VALID_PASSWORD)
        assert login_page.is_error_displayed(), "应该显示用户锁定错误"
        
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower(), "应该显示用户锁定错误信息"
        
        # 清空输入框并成功登录
        login_page.clear_username()
        login_page.clear_password()
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        
        assert products_page.is_products_page(), "应该成功登录到产品页面"
    
    @pytest.mark.regression
    def test_multiple_user_scenarios(self, driver):
        """测试多用户场景（模拟不同用户类型）"""
        from login_page import LoginPage
        from products_page import ProductsPage
        
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        
        # 测试标准用户
        login_page.open(Config.BASE_URL)
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        assert products_page.is_products_page(), "标准用户应该能够登录"
        
        # 添加商品并登出
        products_page.add_backpack_to_cart()
        assert products_page.get_cart_items_count() == 1, "标准用户应该能够添加商品"
        products_page.logout()
        
        # 测试锁定用户
        login_page.login(Config.LOCKED_USERNAME, Config.VALID_PASSWORD)
        assert login_page.is_error_displayed(), "锁定用户应该无法登录"
        assert "locked out" in login_page.get_error_message().lower(), "应该显示锁定错误"
        
        # 清空并重新测试标准用户
        login_page.clear_username()
        login_page.clear_password()
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        assert products_page.is_products_page(), "标准用户应该能够重新登录"
    
    @pytest.mark.performance
    def test_page_load_performance(self, login_page, products_page, cart_page):
        """测试页面加载性能（基础测试）"""
        import time
        
        # 测试登录页面加载
        start_time = time.time()
        login_page.wait_for_page_load()
        login_load_time = time.time() - start_time
        assert login_load_time < 10, f"登录页面加载时间过长: {login_load_time}秒"
        
        # 测试登录过程
        start_time = time.time()
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        products_page.wait_for_page_load()
        login_process_time = time.time() - start_time
        assert login_process_time < 15, f"登录过程时间过长: {login_process_time}秒"
        
        # 测试产品页面操作
        start_time = time.time()
        products_page.add_backpack_to_cart()
        products_page.click_cart_icon()
        cart_page.wait_for_page_load()
        cart_navigation_time = time.time() - start_time
        assert cart_navigation_time < 10, f"购物车导航时间过长: {cart_navigation_time}秒"
        
        print(f"性能测试结果:")
        print(f"  登录页面加载: {login_load_time:.2f}秒")
        print(f"  登录过程: {login_process_time:.2f}秒")
        print(f"  购物车导航: {cart_navigation_time:.2f}秒")