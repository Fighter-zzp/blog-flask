# flask 小案例
### 使用flask实现小博客
* 注册
* 登录
* 保存session
* 添加博客内容
* 修改博客
* 删除博客

### 测试flask 博客
使用`pytest`来运行测试。该命令会找到并且运行所有测试。
```
$ pytest

========================= test session starts ==========================
platform linux -- Python 3.6.4, pytest-3.5.0, py-1.5.3, pluggy-0.6.0
rootdir: /home/user/Projects/flask-tutorial, inifile: setup.cfg
collected 23 items

tests/test_auth.py ........                                      [ 34%]
tests/test_blog.py ............                                  [ 86%]
tests/test_db.py ..                                              [ 95%]
tests/test_factory.py ..                                         [100%]

====================== 24 passed in 0.64 seconds =======================
```
如果有测试失败， `pytest` 会显示引发的错误。可以使用 `pytest -v` 得到每个测试的列表，而不是一串点。

可以使用 `coverage` 命令代替直接使用 `pytest` 来运行测试，这样可以衡量测试 覆盖率。

`$ coverage run -m pytest`  
在终端中，可以看到一个简单的覆盖率报告：
```
$ coverage report

Name                 Stmts   Miss Branch BrPart  Cover
------------------------------------------------------
flaskr/__init__.py      21      0      2      0   100%
flaskr/auth.py          54      0     22      0   100%
flaskr/blog.py          54      0     16      0   100%
flaskr/db.py            24      0      4      0   100%
------------------------------------------------------
TOTAL                  153      0     44      0   100%
```
还可以生成 HTML 报告，可以看到每个文件中测试覆盖了哪些行：
```
$ coverage html
```
这个命令在 htmlcov 文件夹中生成测试报告，然后在浏览器中打开 htmlcov/index.html 查看。