from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from datetime import datetime
from utils import db
from utils import id
from utils import redis_conn
import redis
import json


od = Blueprint('order', __name__)



@od.route('/order_list', methods=['GET'])
def order_list():
    #通过判断用户角色，显示不同订单列表
    #获取session信息
    user_info = session.get('user_info')
    print(f"用户信息：{user_info},type:{type(user_info)}")
    #判断用户是否登录
    if not user_info or not user_info.get('mobile'):
        return redirect(url_for('account.login'))
        #获取用户角色、手机号、用户id
    user_role = user_info.get('role')
    mobile = user_info.get('mobile')
    user_id = user_info.get('user_id')
    print(f"用户角色：{user_role}")
    print(f"用户手机号：{mobile}")
    print(f"用户id：{user_id}")
    #根据用户角色，显示不同订单列表
    if str(user_role) == '2':
        #此处希望在前端显示用户名，进行关联查询，显示用户名称而不是id
        all_order = db.fetch_all('SELECT * FROM Orders left join username on Orders.user_id = username.user_id WHERE user_id=%s', (user_info.get('user_id'),))
        print(all_order, type(all_order))
        #创建状态字典，并且传给前端
        status_dict = {1: '待处理', 2: '执行中', 3: '已完成', 4: '已取消'}
        return render_template('order_list.html', all_order=all_order, status_dict=status_dict)
    if str(user_role) == '1':
        all_order = db.fetch_all('SELECT * FROM Orders left join username on Orders.user_id = username.user_id', ())
        print(all_order)
        status_dict = {1: '待处理',2: '执行中', 3: '已完成', 4: '已取消'}
        return render_template('order_list.html', all_order=all_order, status_dict=status_dict)
    return redirect(url_for('account.login'))


@od.route('/get_products', methods=['GET'])
def get_products():

    import urllib.parse

    # 使用 request.query_string 获取原始查询字符串
    query_string = request.query_string.decode('utf-8')
    print(f"原始查询字符串: {query_string}")

    # 手动解析查询字符串
    params = urllib.parse.parse_qs(query_string)
    search = params.get('search', [''])[0]
    print(f"解析后搜索参数: {search}")

    if not search:
        products_list = db.fetch_all('SELECT * FROM products', ())
        return render_template('products.html', products_list=products_list)

    print(f"执行搜索: {search}")
    products_list = db.fetch_all('SELECT * FROM products WHERE name LIKE %s', ('%' + search + '%',))
    print(f"搜索结果: {products_list}")
    return render_template('products.html', products_list=products_list)



@od.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    #当用户访问该页面时，显示创建订单表单
    if request.method == 'GET':
        return render_template('create_order.html')
    if request.method == 'POST':
        url = request.form.get('url')
        count = request.form.get('count')
        platform = request.form.get('platform')
        if not all([url, count, platform]):
            flash('请填写完整信息')
            return redirect(url_for('order./orders/create'))

    #获取session信息
    user_info = session.get('user_info')
    print(f"用户信息：{user_info},type:{type(user_info)}")

    if not user_info or not user_info.get('mobile'):
        return redirect(url_for('account.login'))
    #获取用户id准备上传
    user_id = user_info.get('user_id')

    print(f"用户id：{user_id}")
    #生成订单id，复用user_id，加上时间戳
    a = id.user_id()
    platform_dict = {
            "抖音":"dy",
            "快手":"ks",
            "哔哩哔哩":"bl",
            "今日头条":"tt",
            "西瓜视频":"xg",

        }
    print(f"平台：{platform_dict.get(platform)}")
    time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = platform_dict.get(platform) + a + time_str
    print(f"订单id：{order_id}")
    #上传订单信息到数据库
    status = 1
    date = datetime.now()#获取当前时间上传数据库
    db.execute('INSERT INTO Orders (order_id, url,count, user_id, status, date,platform) VALUES (%s, %s, %s, %s, %s, %s, %s)', (order_id, url, count, user_id, status, date,platform))
    flash('订单创建成功')
    #创建订单后，将订单信息上传到redis队列
    redis_conn.push_data('order_queue', order_id=order_id, url=url, count=count, status=status,platform=platform)
    flash('订单创建成功')
    #创建订单后，跳转到订单列表页面
    return redirect(url_for('order.order_list'))


