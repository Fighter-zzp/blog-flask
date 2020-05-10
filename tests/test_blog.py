import pytest
from blog.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert "登录".encode() in response.data
    assert "注册".encode() in response.data

    auth.login()
    response = client.get('/')
    assert '注销'.encode() in response.data
    assert 'test title'.encode() in response.data
    assert 'by test on 2020-05-10'.encode() in response.data
    assert 'test\nbody'.encode() in response.data
    assert 'href="/1/update"'.encode() in response.data


@pytest.mark.parametrize('path', (
        '/create',
        '/1/update',
        '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # 将帖子作者更改为其他用户
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # 当前用户无法修改其他用户的信息
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # 当前用户看不到编辑链接
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
        '/2/update',
        '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
        '/create',
        '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert '标题不可无'.encode() in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None
