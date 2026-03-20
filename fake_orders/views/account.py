
from flask import Blueprint, render_template, redirect, url_for, flash, request,session
import logging
from utils import db#导入db文件
from utils import id #导入id文件
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
ac = Blueprint('account', __name__)


products_list = db.fetch_all('SELECT * FROM products', ())
price = products_list[0].get('price')
print(price)
print(products_list)


#登录路由，GET请求返回登录页面，POST请求处理登录请求
@ac.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html',error=None)
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    print(f"用户请求登录，手机号：{mobile}，密码：{password}")
    if not all([mobile,password]):
        return '请输入手机号和密码',400

    user = db.fetch_one('SELECT * FROM username WHERE mobile=%s', (mobile,))
    print(f"查询用户信息结果：{user}")
    if not user:
        return render_template('login.html', error='未查询到账户信息')
    if not check_password_hash(user['password'], password):
        return render_template('login.html', error='密码错误，请重试')


    else:
        session['user_info']={"mobile":user['mobile'],"real_name":user['real_name'],"role":user['role'],"user_id":user['user_id']}#保存用户信息到session
        return render_template('products.html',products_list=products_list)


#注册路由，GET请求返回注册页面，POST请求处理注册请求
@ac.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user_name = request.form.get('user_name')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    if not all([user_name,mobile,password,password_confirm]):
        return '请输入完整信息',400
    if password != password_confirm:
        return '两次输入的密码不一致',400
    hashed_password = generate_password_hash(password)
    while True:
        try:
            user_id = id.user_id()
            db.execute('INSERT INTO username (user_id,mobile,password,real_name) VALUES (%s,%s,%s,%s)', (user_id,mobile,hashed_password,user_name))
            break
        except pymysql.err.IntegrityError:
            continue
    return redirect(url_for('account.login'))










