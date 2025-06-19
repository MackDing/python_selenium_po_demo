# -*- coding: utf-8 -*-
"""
Pages Package

这个包包含了所有的页面对象类，使用Page Object模式实现。
"""

from .base_page import BasePage
from .login_page import LoginPage
from .products_page import ProductsPage
from .cart_page import CartPage

__all__ = [
    'BasePage',
    'LoginPage',
    'ProductsPage',
    'CartPage'
]