# Python Selenium PO Demo

这是一个使用Python + Selenium + Page Object模式的自动化测试演示项目，使用uv进行Python环境管理。

## 项目概述

本项目演示了如何使用Page Object模式构建可维护的Selenium自动化测试框架。测试目标网站为 [Sauce Demo](https://www.saucedemo.com)。

## 技术栈

- **Python 3.8+**: 编程语言
- **Selenium 4.15+**: Web自动化测试框架
- **pytest**: 测试框架
- **uv**: Python包管理工具
- **webdriver-manager**: 自动管理浏览器驱动
- **pytest-html**: 生成HTML测试报告

## 项目结构

```
python_selenium_po_demo/
├── README.md                 # 项目说明文档
├── pyproject.toml           # 项目配置和依赖管理
├── config.py                # 测试配置文件
├── demo.py                  # 项目功能演示脚本
├── pages/                   # 页面对象目录
│   ├── __init__.py          # 页面包初始化文件
│   ├── base_page.py         # 基础页面类
│   ├── login_page.py        # 登录页面对象
│   ├── products_page.py     # 产品页面对象
│   └── cart_page.py         # 购物车页面对象
├── tests/                   # 测试用例目录
│   ├── __init__.py
│   ├── conftest.py          # pytest配置和夹具
│   ├── test_login.py        # 登录功能测试
│   ├── test_products.py     # 产品页面测试
│   ├── test_cart.py         # 购物车功能测试
│   └── test_e2e.py          # 端到端测试
└── reports/                 # 测试报告目录（自动生成）
```

## 环境设置

### 1. 安装uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用pip安装
pip install uv
```

### 2. 安装项目依赖

```bash
# 进入项目目录
cd python_selenium_po_demo

# 安装依赖
uv sync

# 或者使用pip安装
uv pip install -e .
```

### 3. 浏览器驱动

项目使用 `webdriver-manager` 自动管理Chrome驱动，无需手动下载。确保系统已安装Chrome浏览器。

### 4. 浏览器配置

项目已配置Chrome浏览器选项以优化测试体验：
- 禁用凭据和密码管理服务
- 隐藏"Chrome正受到自动测试软件的控制"信息栏
- 支持无头模式运行
- 添加安全和性能优化参数

## 快速演示

### 运行演示脚本

项目提供了一个完整的功能演示脚本 `demo.py`，展示了完整的用户购物流程：

```bash
# 运行演示脚本
uv run python demo.py
```

演示脚本包含以下功能：
- 用户登录
- 浏览产品页面
- 添加商品到购物车
- 查看购物车
- 继续购物
- 用户登出

## 运行测试

### 基本运行命令

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_login.py

# 运行特定测试类
uv run pytest tests/test_login.py::TestLogin

# 运行特定测试方法
uv run pytest tests/test_login.py::TestLogin::test_valid_login
```

### 使用标记运行测试

```bash
# 运行冒烟测试
uv run pytest -m smoke

# 运行回归测试
uv run pytest -m regression

# 运行登录相关测试
uv run pytest -m login

# 运行购物车相关测试
uv run pytest -m cart
```

### 生成测试报告

```bash
# 生成HTML报告
uv run pytest --html=reports/report.html --self-contained-html

# 显示详细输出
uv run pytest -v

# 显示测试覆盖率（需要安装pytest-cov）
uv run pytest --cov=. --cov-report=html
```

### 环境变量配置

```bash
# 设置浏览器类型（默认chrome）
export BROWSER=chrome

# 启用无头模式
export HEADLESS=true

# 运行测试
uv run pytest
```

## Page Object模式说明

### 基础页面类 (BasePage)

位于 `pages/base_page.py`，提供所有页面对象的通用方法：
- 元素查找和操作
- 等待机制
- 通用页面操作

### 页面对象类

所有页面对象类都位于 `pages/` 目录下：
- **LoginPage** (`pages/login_page.py`): 登录页面操作
- **ProductsPage** (`pages/products_page.py`): 产品页面操作
- **CartPage** (`pages/cart_page.py`): 购物车页面操作

### 页面包导入

通过 `pages/__init__.py` 统一管理页面对象的导入：
```python
from pages import LoginPage, ProductsPage, CartPage
```

### 测试用例组织

- **test_login.py**: 登录功能的各种场景测试
- **test_products.py**: 产品浏览、添加到购物车等功能测试
- **test_cart.py**: 购物车操作功能测试
- **test_e2e.py**: 端到端完整流程测试

## 测试数据

### 有效用户
- 用户名: `standard_user`
- 密码: `secret_sauce`

### 测试用户类型
- `standard_user`: 标准用户
- `locked_out_user`: 被锁定用户
- `problem_user`: 问题用户
- `performance_glitch_user`: 性能问题用户
- `error_user`: 错误用户
- `visual_user`: 视觉用户

## 最佳实践

### 1. 项目结构组织
- 使用 `pages/` 目录集中管理所有页面对象
- 通过 `__init__.py` 统一管理页面对象导入
- 保持清晰的目录层次结构

### 2. Page Object模式
- 每个页面一个类
- 封装页面元素和操作
- 提供业务级别的方法
- 继承基础页面类复用通用功能

### 3. 测试数据管理
- 使用配置文件管理测试数据
- 避免硬编码
- 使用夹具提供测试数据

### 4. 等待策略
- 使用显式等待而非隐式等待
- 等待元素可见而非仅存在
- 合理设置超时时间

### 5. 测试组织
- 使用pytest标记分类测试
- 合理使用夹具
- 保持测试独立性

### 6. 浏览器配置
- 配置Chrome选项优化测试体验
- 支持无头模式和CI/CD环境
- 禁用不必要的浏览器功能

## 常见问题

### 1. Chrome驱动问题
```bash
# 如果遇到驱动问题，可以手动更新
uv run python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### 2. 权限问题
```bash
# macOS可能需要允许Chrome驱动运行
sudo xattr -d com.apple.quarantine /path/to/chromedriver
```

### 3. 无头模式问题
```bash
# 如果无头模式有问题，可以关闭无头模式调试
export HEADLESS=false
uv run pytest
```

## 扩展功能

### 添加新页面对象
1. 继承 `BasePage` 类
2. 定义页面元素定位器
3. 实现页面特定的操作方法
4. 编写对应的测试用例

### 添加新测试
1. 在 `tests/` 目录下创建测试文件
2. 使用适当的pytest标记
3. 利用现有的夹具
4. 遵循命名规范

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目仅用于学习和演示目的。

## 联系方式

如有问题或建议，请创建Issue或联系项目维护者。