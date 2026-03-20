# Flask Order 系统

## 项目介绍

Flask Order 是一个基于 Flask 框架开发的订单管理系统，主要用于管理和处理各类平台的订单。系统支持用户认证、订单创建、订单管理等功能，并集成了数据库连接池和 Redis 队列等技术，提高系统性能和可靠性。

## 功能特性

- **用户认证**：支持用户注册和登录功能，使用密码哈希加密确保安全
- **订单管理**：支持创建订单、查看订单列表，区分不同角色的订单视图
- **产品管理**：支持查看产品列表、搜索产品功能
- **权限控制**：基于用户角色的权限管理，不同角色查看不同的订单列表
- **数据库优化**：使用连接池机制，减少数据库连接开销
- **消息队列**：集成 Redis 队列，用于订单处理和异步任务

## 技术栈

- **后端**：Python 3.8+, Flask 框架
- **数据库**：MySQL
- **缓存**：Redis
- **前端**：HTML, Bootstrap 5
- **其他**：pymysql, dbutils, werkzeug

## 目录结构

```
flask_order/
├── app.py                    # 应用入口文件
├── fake_orders/              # 核心应用模块
│   ├── __init__.py           # 应用初始化
│   ├── templates/            # 前端模板
│   │   ├── login.html        # 登录页面
│   │   ├── register.html     # 注册页面
│   │   ├── products.html     # 产品列表页面
│   │   ├── create_order.html # 创建订单页面
│   │   └── order_list.html   # 订单列表页面
│   └── views/                # 视图模块
│       ├── account.py        # 账户相关视图
│       └── order.py          # 订单相关视图
├── utils/                    # 工具模块
│   ├── db.py                 # 数据库操作
│   ├── id.py                 # ID 生成
│   └── redis_conn.py         # Redis 连接
├── static/                   # 静态文件
├── .venv/                    # 虚拟环境
├── venv/                     # 虚拟环境
├── .gitignore                # Git 忽略文件
└── README.md                 # 项目文档
```

## 安装步骤

### 1. 克隆项目

```bash
git clone <项目地址>
cd flask_order
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install flask pymysql dbutils redis werkzeug
```

### 3. 数据库配置

1. 创建数据库

```sql
CREATE DATABASE fake_orders CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 创建表结构

```sql
-- 用户表
CREATE TABLE username (
    user_id VARCHAR(20) PRIMARY KEY,
    mobile VARCHAR(11) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    real_name VARCHAR(50) NOT NULL,
    role INT DEFAULT 2 -- 1: 管理员, 2: 普通用户
);

-- 产品表
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT
);

-- 订单表
CREATE TABLE Orders (
    order_id VARCHAR(50) PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    count INT NOT NULL,
    user_id VARCHAR(20) NOT NULL,
    status INT DEFAULT 1, -- 1: 待处理, 2: 执行中, 3: 已完成, 4: 已取消
    date DATETIME NOT NULL,
    platform VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES username(user_id)
);
```

3. 修改数据库连接配置

编辑 `utils/db.py` 文件，修改数据库连接参数：

```python
POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    setsession=[],
    ping=0,
    host='localhost',
    port=3306,
    user='root',
    password='your_password',  # 修改为你的数据库密码
    database='fake_orders',
    charset='utf8mb4'
)
```

### 4. Redis 配置

确保 Redis 服务已启动，默认配置为本地 6379 端口。如需修改 Redis 连接配置，编辑 `utils/redis_conn.py` 文件。

## 使用方法

### 1. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

### 2. 访问流程

1. **注册**：访问 `http://localhost:5000/register` 注册新用户
2. **登录**：访问 `http://localhost:5000/login` 登录系统
3. **查看产品**：登录后自动跳转到产品列表页面
4. **创建订单**：点击 "创建订单" 按钮，填写订单信息
5. **查看订单**：点击 "订单列表" 查看已创建的订单

## 系统架构

### 核心模块

1. **应用初始化**：`fake_orders/__init__.py` 中创建 Flask 应用，注册蓝图，设置认证中间件
2. **用户认证**：`views/account.py` 处理用户注册和登录
3. **订单管理**：`views/order.py` 处理订单创建和查看
4. **数据库操作**：`utils/db.py` 提供数据库连接池和操作方法
5. **Redis 队列**：`utils/redis_conn.py` 提供 Redis 连接和队列操作

### 认证流程

1. 用户访问需要认证的页面
2. 中间件 `auth()` 检查用户是否登录
3. 未登录用户重定向到登录页面
4. 登录成功后，用户信息存储在 session 中
5. 后续请求通过 session 验证用户身份

### 订单处理流程

1. 用户创建订单，填写 URL、数量和平台
2. 系统生成订单 ID，保存到数据库
3. 订单信息同时推送到 Redis 队列
4. 后台处理程序从队列中获取订单并处理

## 注意事项

1. **数据库配置**：确保数据库服务已启动，且连接参数正确
2. **Redis 服务**：确保 Redis 服务已启动，用于订单队列处理
3. **安全配置**：生产环境中应修改 `app.secret_key` 为随机字符串
4. **依赖安装**：确保所有依赖已正确安装
5. **端口冲突**：如果 5000 端口被占用，可以修改 `app.py` 中的端口号

## 扩展建议

1. **添加订单状态更新功能**
2. **实现订单搜索和筛选功能**
3. **添加用户权限管理界面**
4. **实现订单统计和报表功能**
5. **添加邮件通知功能**
6. **优化前端界面，提升用户体验**

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系项目维护者。
