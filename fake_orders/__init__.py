from flask import Flask, request, redirect, url_for, session

def auth():
    print(request.path)
    if request.path.startswith('/static/'):#如果是静态文件，则不进行认证
        return None
    if request.path == "https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/css/bootstrap.min.css":#如果是bootstrap的css文件，则不进行认证
        return None
    if request.path == "https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/js/bootstrap.bundle.min.js":#如果是bootstrap的js文件，则不进行认证
        return None
    if request.path == '/login' or request.path == '/register':#如果是登录页面或注册页面，则不进行认证
        return None
    user_info = session.get('user_info')#获取session中的用户信息
    if not user_info:
        return redirect(url_for('account.login'))#如果没有获取到session，则跳转到登录页面
    return None



def create_app():
    import os
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    app.secret_key = '123456'#设置session密钥，用于加密session数据,加盐动作


    from .views import account
    app.register_blueprint(account.ac)#蓝图注册
    from .views import order
    app.register_blueprint(order.od)

    app.before_request(auth)

    return app
