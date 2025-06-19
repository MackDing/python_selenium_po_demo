"""产品页面功能测试用例"""

import pytest
from config import Config


class TestProducts:
    """产品页面功能测试类"""
    
    @pytest.mark.smoke
    def test_products_page_display(self, logged_in_user):
        """测试产品页面显示"""
        # 验证页面基本元素
        assert logged_in_user.is_products_page(), "应该在产品页面"
        assert "Products" in logged_in_user.get_page_title_text(), "页面标题应该包含'Products'"
        
        # 验证产品数量
        products_count = logged_in_user.get_products_count()
        assert products_count > 0, "应该显示至少一个产品"
        assert products_count == 6, f"应该显示6个产品，实际显示{products_count}个"
    
    def test_product_information_display(self, logged_in_user):
        """测试产品信息显示"""
        # 获取产品名称
        product_names = logged_in_user.get_product_names()
        assert len(product_names) > 0, "应该显示产品名称"
        
        # 验证特定产品存在
        expected_products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]
        
        for product in expected_products:
            assert product in product_names, f"产品'{product}'应该在产品列表中"
        
        # 获取产品价格
        product_prices = logged_in_user.get_product_prices()
        assert len(product_prices) > 0, "应该显示产品价格"
        assert len(product_prices) == len(product_names), "产品价格数量应该与产品名称数量一致"
        
        # 验证价格格式
        for price in product_prices:
            assert price.startswith('$'), f"价格应该以$开头: {price}"
            # 验证价格是有效数字
            price_value = price.replace('$', '')
            assert float(price_value) > 0, f"价格应该大于0: {price}"
    
    @pytest.mark.cart
    def test_add_single_product_to_cart(self, logged_in_user):
        """测试添加单个产品到购物车"""
        # 初始购物车应该为空
        initial_cart_count = logged_in_user.get_cart_items_count()
        assert initial_cart_count == 0, "初始购物车应该为空"
        
        # 添加背包到购物车
        logged_in_user.add_backpack_to_cart()
        
        # 验证购物车数量增加
        cart_count = logged_in_user.get_cart_items_count()
        assert cart_count == 1, "购物车应该有1个商品"
        
        # 验证产品状态变为已添加
        assert logged_in_user.is_product_added_to_cart("sauce-labs-backpack"), "背包应该显示为已添加到购物车"
    
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, logged_in_user):
        """测试添加多个产品到购物车"""
        # 添加多个产品
        logged_in_user.add_backpack_to_cart()
        logged_in_user.add_bike_light_to_cart()
        logged_in_user.add_bolt_tshirt_to_cart()
        
        # 验证购物车数量
        cart_count = logged_in_user.get_cart_items_count()
        assert cart_count == 3, "购物车应该有3个商品"
        
        # 验证所有产品都显示为已添加
        assert logged_in_user.is_product_added_to_cart("sauce-labs-backpack"), "背包应该已添加"
        assert logged_in_user.is_product_added_to_cart("sauce-labs-bike-light"), "自行车灯应该已添加"
        assert logged_in_user.is_product_added_to_cart("sauce-labs-bolt-t-shirt"), "T恤应该已添加"
    
    @pytest.mark.cart
    def test_remove_product_from_cart(self, logged_in_user):
        """测试从购物车移除产品"""
        # 先添加产品
        logged_in_user.add_backpack_to_cart()
        logged_in_user.add_bike_light_to_cart()
        assert logged_in_user.get_cart_items_count() == 2, "应该有2个商品在购物车中"
        
        # 移除一个产品
        logged_in_user.remove_product_from_cart_by_name("sauce-labs-backpack")
        
        # 验证购物车数量减少
        cart_count = logged_in_user.get_cart_items_count()
        assert cart_count == 1, "购物车应该还有1个商品"
        
        # 验证产品状态变为未添加
        assert not logged_in_user.is_product_added_to_cart("sauce-labs-backpack"), "背包应该显示为未添加"
        assert logged_in_user.is_product_added_to_cart("sauce-labs-bike-light"), "自行车灯应该仍在购物车中"
    
    def test_cart_icon_navigation(self, logged_in_user, cart_page):
        """测试购物车图标导航"""
        # 添加产品到购物车
        logged_in_user.add_backpack_to_cart()
        
        # 点击购物车图标
        logged_in_user.click_cart_icon()
        
        # 验证跳转到购物车页面
        assert cart_page.is_cart_page(), "应该跳转到购物车页面"
    
    def test_product_sorting(self, logged_in_user):
        """测试产品排序功能"""
        # 获取默认排序的产品名称
        default_names = logged_in_user.get_product_names()
        
        # 按名称Z到A排序
        logged_in_user.select_sort_option("za")
        za_names = logged_in_user.get_product_names()
        
        # 验证排序结果
        assert za_names != default_names, "Z到A排序后产品顺序应该改变"
        assert za_names == sorted(default_names, reverse=True), "Z到A排序结果不正确"
        
        # 按名称A到Z排序
        logged_in_user.select_sort_option("az")
        az_names = logged_in_user.get_product_names()
        
        # 验证排序结果
        assert az_names == sorted(default_names), "A到Z排序结果不正确"
    
    def test_price_sorting(self, logged_in_user):
        """测试价格排序功能"""
        # 按价格从低到高排序
        logged_in_user.select_sort_option("lohi")
        lohi_prices = logged_in_user.get_product_prices()
        
        # 转换价格为数字进行比较
        lohi_values = [float(price.replace('$', '')) for price in lohi_prices]
        assert lohi_values == sorted(lohi_values), "价格从低到高排序不正确"
        
        # 按价格从高到低排序
        logged_in_user.select_sort_option("hilo")
        hilo_prices = logged_in_user.get_product_prices()
        
        # 转换价格为数字进行比较
        hilo_values = [float(price.replace('$', '')) for price in hilo_prices]
        assert hilo_values == sorted(hilo_values, reverse=True), "价格从高到低排序不正确"
    
    @pytest.mark.regression
    def test_menu_functionality(self, logged_in_user, login_page):
        """测试菜单功能"""
        # 点击菜单按钮
        logged_in_user.click_menu_button()
        
        # 执行登出
        logged_in_user.logout()
        
        # 验证登出成功
        assert login_page.is_login_page(), "应该跳转到登录页面"
    
    @pytest.mark.parametrize("product_name,button_method", [
        ("sauce-labs-backpack", "add_backpack_to_cart"),
        ("sauce-labs-bike-light", "add_bike_light_to_cart"),
        ("sauce-labs-bolt-t-shirt", "add_bolt_tshirt_to_cart")
    ])
    def test_individual_product_addition(self, logged_in_user, product_name, button_method):
        """参数化测试各个产品的添加功能"""
        # 获取添加方法
        add_method = getattr(logged_in_user, button_method)
        
        # 添加产品
        add_method()
        
        # 验证产品已添加
        assert logged_in_user.get_cart_items_count() == 1, "购物车应该有1个商品"
        assert logged_in_user.is_product_added_to_cart(product_name), f"产品{product_name}应该已添加到购物车"
    
    def test_cart_badge_display(self, logged_in_user):
        """测试购物车徽章显示"""
        # 初始状态购物车徽章不应该显示
        assert logged_in_user.get_cart_items_count() == 0, "初始购物车应该为空"
        
        # 添加1个产品
        logged_in_user.add_backpack_to_cart()
        assert logged_in_user.get_cart_items_count() == 1, "购物车徽章应该显示1"
        
        # 添加更多产品
        logged_in_user.add_bike_light_to_cart()
        logged_in_user.add_bolt_tshirt_to_cart()
        assert logged_in_user.get_cart_items_count() == 3, "购物车徽章应该显示3"
        
        # 移除产品
        logged_in_user.remove_product_from_cart_by_name("sauce-labs-backpack")
        assert logged_in_user.get_cart_items_count() == 2, "购物车徽章应该显示2"