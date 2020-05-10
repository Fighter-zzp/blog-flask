"""
认证蓝图
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from blog.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        err = None

        if not username:
            err = '用户名是必须的'
        elif not password:
            err = '密码是必须的'
        elif db.execute('SELECT id FROM user WHERE username = ?',
                        (username,)).fetchone() is not None:
            err = '用户名{} 已经存在'.format(username)

        if err is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(err)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        err = None
        # 查询并获取用户
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)
                          ).fetchone()
        # 验证不正确
        if user is None:
            err = '用户名不正确'
        elif not check_password_hash(user['password'], password):
            err = '密码不正确'
        # 存进session
        if err is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(err)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    加载已登录用户
    :return:
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用装饰器来完成这个工作。
    :param view: 视图
    :return:
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
