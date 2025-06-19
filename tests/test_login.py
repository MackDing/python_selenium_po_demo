"""登录功能测试用例"""

import pytest
from config import Config


class TestLogin:
    """登录功能测试类"""
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, login_page, products_page):
        """测试有效用户登录"""
        # 执行登录
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        
        # 验证登录成功
        assert products_page.is_products_page(), "登录失败，未跳转到产品页面"
        assert "Products" in products_page.get_page_title_text(), "页面标题不正确"
        assert products_page.get_products_count() > 0, "产品页面没有显示任何产品"
    
    @pytest.mark.login
    def test_locked_user_login(self, login_page):
        """测试被锁定用户登录"""
        # 执行登录
        login_page.login(Config.LOCKED_USERNAME, Config.VALID_PASSWORD)
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_invalid_username_login(self, login_page):
        """测试无效用户名登录"""
        # 执行登录
        login_page.login(Config.INVALID_USERNAME, Config.VALID_PASSWORD)
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "do not match" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_invalid_password_login(self, login_page):
        """测试无效密码登录"""
        # 执行登录
        login_page.login(Config.VALID_USERNAME, Config.INVALID_PASSWORD)
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "do not match" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_empty_username_login(self, login_page):
        """测试空用户名登录"""
        # 执行登录
        login_page.login("", Config.VALID_PASSWORD)
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "username is required" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_empty_password_login(self, login_page):
        """测试空密码登录"""
        # 执行登录
        login_page.login(Config.VALID_USERNAME, "")
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "password is required" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_empty_credentials_login(self, login_page):
        """测试空用户名和密码登录"""
        # 执行登录
        login_page.login("", "")
        
        # 验证登录失败
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message()
        assert "username is required" in error_message.lower(), f"错误信息不正确: {error_message}"
        assert login_page.is_login_page(), "应该仍在登录页面"
    
    @pytest.mark.login
    def test_error_message_close(self, login_page):
        """测试关闭错误信息"""
        # 触发错误信息
        login_page.login("", "")
        assert login_page.is_error_displayed(), "应该显示错误信息"
        
        # 关闭错误信息
        login_page.close_error_message()
        
        # 验证错误信息已关闭
        assert not login_page.is_error_displayed(), "错误信息应该已关闭"
    
    @pytest.mark.login
    def test_input_field_operations(self, login_page):
        """测试输入框操作"""
        # 输入用户名
        test_username = "test_user"
        login_page.enter_username(test_username)
        assert login_page.get_username_value() == test_username, "用户名输入不正确"
        
        # 输入密码
        test_password = "test_password"
        login_page.enter_password(test_password)
        assert login_page.get_password_value() == test_password, "密码输入不正确"
        
        # 清空用户名
        login_page.clear_username()
        assert login_page.get_username_value() == "", "用户名应该已清空"
        
        # 清空密码
        login_page.clear_password()
        assert login_page.get_password_value() == "", "密码应该已清空"
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_logout_functionality(self, logged_in_user, login_page):
        """测试登出功能"""
        # 执行登出
        logged_in_user.logout()
        
        # 验证登出成功
        assert login_page.is_login_page(), "登出失败，未跳转到登录页面"
        
        # 验证无法直接访问产品页面
        logged_in_user.driver.get(Config.BASE_URL + "/inventory.html")
        assert login_page.is_login_page(), "登出后应该无法直接访问产品页面"
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "", "username is required"),
        ("valid_user", "", "password is required"),
        ("", "valid_pass", "username is required"),
        ("invalid_user", "invalid_pass", "do not match"),
        (Config.LOCKED_USERNAME, Config.VALID_PASSWORD, "locked out")
    ])
    def test_login_error_scenarios(self, login_page, username, password, expected_error):
        """参数化测试登录错误场景"""
        login_page.login(username, password)
        
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_message = login_page.get_error_message().lower()
        assert expected_error in error_message, f"期望错误信息包含'{expected_error}'，实际错误信息: {error_message}"