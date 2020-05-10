import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    获取数据库
    :return:
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    关闭数据库
    :return:
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    初始化数据库
    :return:
    """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    初始化数据库命令
    :return:
    """
    init_db()
    click.echo('初始化数据库.')


def init_app(app):
    """
    注册close_db和init_db_command
    :param app: flask app实例
    :return:
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
