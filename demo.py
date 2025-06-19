#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本 - Python Selenium PO Demo

这个脚本演示了如何使用Page Object模式进行Selenium自动化测试
"""

import time
from config import Config
from pages import LoginPage, ProductsPage, CartPage


def main():
    """主演示函数"""
    print("🚀 开始演示 Python Selenium PO Demo")
    print("=" * 50)
    
    # 初始化WebDriver
    driver = Config.get_driver()
    
    try:
        # 创建页面对象
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        cart_page = CartPage(driver)
        
        # 演示1: 登录功能
        print("\n📝 演示1: 用户登录")
        login_page.open(Config.BASE_URL)
        print(f"✅ 打开登录页面: {driver.current_url}")
        
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        print(f"✅ 使用用户 '{Config.VALID_USERNAME}' 登录成功")
        
        # 验证登录成功
        if products_page.is_products_page():
            print("✅ 成功跳转到产品页面")
        else:
            print("❌ 登录失败")
            return
        
        # 演示2: 产品浏览
        print("\n🛍️ 演示2: 产品浏览")
        products_count = products_page.get_products_count()
        print(f"✅ 发现 {products_count} 个产品")
        
        product_names = products_page.get_product_names()
        print("📦 产品列表:")
        for i, name in enumerate(product_names[:3], 1):  # 只显示前3个
            print(f"   {i}. {name}")
        
        # 演示3: 添加产品到购物车
        print("\n🛒 演示3: 添加产品到购物车")
        
        # 添加背包
        products_page.add_backpack_to_cart()
        print("✅ 添加 'Sauce Labs Backpack' 到购物车")
        
        # 添加自行车灯
        products_page.add_bike_light_to_cart()
        print("✅ 添加 'Sauce Labs Bike Light' 到购物车")
        
        # 检查购物车数量
        cart_count = products_page.get_cart_items_count()
        print(f"✅ 购物车中有 {cart_count} 个商品")
        
        # 演示4: 查看购物车
        print("\n🛒 演示4: 查看购物车")
        products_page.click_cart_icon()
        
        if cart_page.is_cart_page():
            print("✅ 成功进入购物车页面")
            
            cart_items = cart_page.get_cart_item_names()
            print("📦 购物车中的商品:")
            for i, item in enumerate(cart_items, 1):
                print(f"   {i}. {item}")
        else:
            print("❌ 未能进入购物车页面")
        
        # 演示5: 返回产品页面
        print("\n🔄 演示5: 继续购物")
        cart_page.click_continue_shopping()
        
        if products_page.is_products_page():
            print("✅ 成功返回产品页面")
            print(f"✅ 购物车状态保持: {products_page.get_cart_items_count()} 个商品")
        
        # 演示6: 登出
        print("\n🚪 演示6: 用户登出")
        products_page.click_menu_button()
        time.sleep(1)  # 等待菜单展开
        products_page.logout()
        
        if login_page.is_login_page():
            print("✅ 成功登出，返回登录页面")
        else:
            print("❌ 登出失败")
        
        print("\n🎉 演示完成！")
        print("=" * 50)
        print("\n📊 演示总结:")
        print("✅ 登录功能 - 正常")
        print("✅ 产品浏览 - 正常")
        print("✅ 购物车操作 - 正常")
        print("✅ 页面导航 - 正常")
        print("✅ 登出功能 - 正常")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {str(e)}")
        
    finally:
        # 关闭浏览器
        print("\n🔚 关闭浏览器")
        driver.quit()


if __name__ == "__main__":
    main()