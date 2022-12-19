# 该模块是服务器模块
# 该模块基于flask框架，搭建了数据库展示前端的WEB服务
# update for fix

import os
from flask import Flask, render_template, request, redirect, session, flash, send_from_directory
from flask.globals import current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import get_last_week
from get_last_week import get_last_week, get_detail_info
from user import User, get_user, create_user
from databaseCURD import getDatabase, commitChangeToDatabase

import getDetailInfo

import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'div'

    login_manager = LoginManager()  # 实例化登录管理对象
    login_manager.init_app(app)  # 初始化应用
    login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint

    @login_manager.user_loader  # 定义获取登录用户的方法
    def load_user(user_id):
        return User.get(user_id)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/yukiyu')
    def index_page():
        return render_template('index.html')

    @app.route('/yukiyu/main')
    def main_page():
        print('main_page func called')
        userame = None
        if hasattr(current_user, 'username'):
            userame = current_user.username
        print('current user: ', userame)
        return render_template('main.html', user=userame)

    # rank tool
    @app.route('/yukiyu/main/rank')
    def rank_tool():
        print('rank tool called')
        return render_template('rank_tool.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html', target='/login', way='登陆')
        if request.method == 'POST':
            user_name = request.form.get('username')
            password = request.form.get('password')
            user_info = get_user(user_name)
            emsg = None
            if user_info is None:
                emsg = '该用户名不存在'
            else:
                user = User(user_info)
                if user.verify_password(password):  # 校验密码
                    login_user(user)  # 创建用户 Session
                else:
                    emsg = "密码有误"

            if emsg is None:
                return redirect(request.args.get('next') or '/yukiyu/main')

            else:
                flash(emsg)
                return redirect('/login')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('login.html', target='/register', way='注册')
        else:
            user_name = request.form.get('username')
            password = request.form.get('password')
            create_user(user_name, password)
            flash('创建用户成功，请登陆')
            return redirect('/login')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/yukiyu')

    @app.route('/yukiyu/database', methods=['GET', 'POST'])
    @login_required
    def database_page():
        if request.method == 'GET':
            agrs = request.args
            if agrs:
                res = getDatabase(agrs, getattr(current_user, 'username', None))
                return res
            return render_template('database.html')
        else:
            res = json.loads(request.data)
            print('get data:')
            print(res)
            returnStatus = commitChangeToDatabase(res['oldInfo'], res['newInfo'], res['tableName'],
                                                  getattr(current_user, 'username', None))
            return returnStatus

    @app.route('/bangumi')
    def get_bangumi_info():
        agrs = request.args
        bangumi = None
        if agrs:
            bangumi = get_detail_info(agrs.get('id'))
        else:
            bangumi = get_last_week()
        return bangumi

    @app.route('/favicon.ico')
    def favicon():
        print('favicon fun called!')
        return current_app.send_static_file('images/favicon.ico')

    @app.route('/Swehominmind/')
    def show_detail():
        return render_template('details.html', title='辉夜大小姐想让我告白', contain='一些介绍')

    @app.route('/rank/')
    def show_rank():
        return render_template('rank.html')

    @app.route('/detailInfo/')
    def detailInfo():
        bangumiId = request.args['id']
        detailInfo = getDetailInfo.getDetailById(bangumiId)
        return detailInfo

    @app.route('/profile/')
    def show_profile():
        username = request.args.get("user", default="未登录", type=str)
        return render_template('profile.html', user=username)

    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"  # 指定浏览器渲染的文件类型，和解码格式；

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=8088,
        debug=True
    )
