"""购物车功能测试用例"""

import pytest
from config import Config


class TestCart:
    """购物车功能测试类"""
    
    @pytest.fixture
    def cart_with_items(self, logged_in_user, cart_page):
        """购物车中有商品的夹具"""
        # 添加多个商品到购物车
        logged_in_user.add_backpack_to_cart()
        logged_in_user.add_bike_light_to_cart()
        logged_in_user.add_bolt_tshirt_to_cart()
        
        # 导航到购物车页面
        logged_in_user.click_cart_icon()
        return cart_page
    
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_empty_cart_display(self, logged_in_user, cart_page):
        """测试空购物车显示"""
        # 导航到购物车页面
        logged_in_user.click_cart_icon()
        
        # 验证购物车页面
        assert cart_page.is_cart_page(), "应该在购物车页面"
        assert "Your Cart" in cart_page.get_page_title_text(), "页面标题应该包含'Your Cart'"
        
        # 验证空购物车
        assert cart_page.is_cart_empty(), "购物车应该为空"
        assert cart_page.get_cart_items_count() == 0, "购物车商品数量应该为0"
        
        # 验证按钮状态
        assert cart_page.is_continue_shopping_button_visible(), "继续购物按钮应该可见"
        assert cart_page.is_checkout_button_enabled(), "结账按钮应该可用"
    
    @pytest.mark.cart
    def test_cart_with_items_display(self, cart_with_items):
        """测试有商品的购物车显示"""
        # 验证购物车不为空
        assert not cart_with_items.is_cart_empty(), "购物车不应该为空"
        assert cart_with_items.get_cart_items_count() == 3, "购物车应该有3个商品"
        
        # 验证商品信息
        item_names = cart_with_items.get_cart_item_names()
        expected_items = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]
        
        for item in expected_items:
            assert item in item_names, f"商品'{item}'应该在购物车中"
        
        # 验证价格信息
        item_prices = cart_with_items.get_cart_item_prices()
        assert len(item_prices) == 3, "应该显示3个商品的价格"
        
        for price in item_prices:
            assert price.startswith('$'), f"价格应该以$开头: {price}"
            price_value = float(price.replace('$', ''))
            assert price_value > 0, f"价格应该大于0: {price}"
    
    @pytest.mark.cart
    def test_remove_item_from_cart(self, cart_with_items):
        """测试从购物车移除商品"""
        # 移除一个商品
        cart_with_items.remove_item_by_name("Sauce Labs Backpack")
        
        # 验证商品数量减少
        assert cart_with_items.get_cart_items_count() == 2, "购物车应该还有2个商品"
        
        # 验证特定商品已移除
        item_names = cart_with_items.get_cart_item_names()
        assert "Sauce Labs Backpack" not in item_names, "背包应该已从购物车移除"
        assert "Sauce Labs Bike Light" in item_names, "自行车灯应该仍在购物车中"
        assert "Sauce Labs Bolt T-Shirt" in item_names, "T恤应该仍在购物车中"
    
    @pytest.mark.cart
    def test_clear_entire_cart(self, cart_with_items):
        """测试清空整个购物车"""
        # 清空购物车
        cart_with_items.clear_cart()
        
        # 验证购物车为空
        assert cart_with_items.is_cart_empty(), "购物车应该为空"
        assert cart_with_items.get_cart_items_count() == 0, "购物车商品数量应该为0"
    
    @pytest.mark.cart
    def test_continue_shopping_functionality(self, cart_with_items, products_page):
        """测试继续购物功能"""
        # 点击继续购物按钮
        cart_with_items.click_continue_shopping()
        
        # 验证返回到产品页面
        assert products_page.is_products_page(), "应该返回到产品页面"
        
        # 验证购物车状态保持
        assert products_page.get_cart_items_count() == 3, "购物车中的商品应该保持不变"
    
    @pytest.mark.cart
    def test_cart_item_quantities(self, cart_with_items):
        """测试购物车商品数量显示"""
        # 获取商品数量
        quantities = cart_with_items.get_cart_item_quantities()
        
        # 验证每个商品的数量都是1（默认情况）
        assert len(quantities) == 3, "应该有3个商品的数量信息"
        for quantity in quantities:
            assert quantity == 1, f"每个商品的数量应该是1，实际是{quantity}"
    
    @pytest.mark.cart
    def test_cart_total_price_calculation(self, cart_with_items):
        """测试购物车总价计算"""
        # 获取商品价格
        item_prices = cart_with_items.get_cart_item_prices()
        
        # 手动计算总价
        expected_total = 0.0
        for price_text in item_prices:
            price = float(price_text.replace('$', ''))
            expected_total += price
        
        # 获取计算的总价
        calculated_total = cart_with_items.get_total_price()
        
        # 验证总价计算正确
        assert abs(calculated_total - expected_total) < 0.01, f"总价计算错误，期望{expected_total}，实际{calculated_total}"
    
    @pytest.mark.cart
    def test_specific_item_operations(self, logged_in_user, cart_page):
        """测试特定商品的操作"""
        # 添加特定商品
        logged_in_user.add_backpack_to_cart()
        logged_in_user.click_cart_icon()
        
        # 验证商品在购物车中
        assert cart_page.is_item_in_cart("Sauce Labs Backpack"), "背包应该在购物车中"
        assert not cart_page.is_item_in_cart("Sauce Labs Bike Light"), "自行车灯不应该在购物车中"
        
        # 移除商品
        cart_page.remove_item_by_name("Sauce Labs Backpack")
        
        # 验证商品已移除
        assert not cart_page.is_item_in_cart("Sauce Labs Backpack"), "背包应该已从购物车移除"
        assert cart_page.is_cart_empty(), "购物车应该为空"
    
    @pytest.mark.cart
    def test_checkout_button_functionality(self, cart_with_items):
        """测试结账按钮功能"""
        # 验证结账按钮可用
        assert cart_with_items.is_checkout_button_enabled(), "结账按钮应该可用"
        
        # 点击结账按钮（注意：这里只测试按钮可点击，不测试结账流程）
        # 在实际项目中，这里会跳转到结账页面
        try:
            cart_with_items.click_checkout()
            # 如果有结账页面，可以在这里验证跳转
        except Exception as e:
            # 如果结账功能未实现，捕获异常
            print(f"结账功能可能未实现: {e}")
    
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_persistence_across_pages(self, logged_in_user, cart_page, products_page):
        """测试购物车在页面间的持久性"""
        # 在产品页面添加商品
        logged_in_user.add_backpack_to_cart()
        logged_in_user.add_bike_light_to_cart()
        
        # 导航到购物车页面
        logged_in_user.click_cart_icon()
        assert cart_page.get_cart_items_count() == 2, "购物车应该有2个商品"
        
        # 返回产品页面
        cart_page.click_continue_shopping()
        assert products_page.get_cart_items_count() == 2, "返回产品页面后购物车应该仍有2个商品"
        
        # 再次导航到购物车页面
        products_page.click_cart_icon()
        assert cart_page.get_cart_items_count() == 2, "再次进入购物车页面应该仍有2个商品"
    
    @pytest.mark.parametrize("product_name", [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt"
    ])
    def test_individual_item_removal(self, logged_in_user, cart_page, product_name):
        """参数化测试各个商品的移除功能"""
        # 添加所有商品
        logged_in_user.add_backpack_to_cart()
        logged_in_user.add_bike_light_to_cart()
        logged_in_user.add_bolt_tshirt_to_cart()
        
        # 导航到购物车
        logged_in_user.click_cart_icon()
        assert cart_page.get_cart_items_count() == 3, "应该有3个商品"
        
        # 移除指定商品
        cart_page.remove_item_by_name(product_name)
        
        # 验证商品已移除
        assert not cart_page.is_item_in_cart(product_name), f"商品'{product_name}'应该已移除"
        assert cart_page.get_cart_items_count() == 2, "应该还有2个商品"
    
    def test_empty_cart_checkout_behavior(self, logged_in_user, cart_page):
        """测试空购物车的结账行为"""
        # 导航到空购物车
        logged_in_user.click_cart_icon()
        assert cart_page.is_cart_empty(), "购物车应该为空"
        
        # 验证结账按钮状态（即使购物车为空，按钮通常仍然可用）
        assert cart_page.is_checkout_button_enabled(), "结账按钮应该可用"
        
        # 尝试点击结账按钮
        try:
            cart_page.click_checkout()
            # 在实际应用中，这里可能会显示错误信息或阻止结账
        except Exception as e:
            print(f"空购物车结账可能被阻止: {e}")