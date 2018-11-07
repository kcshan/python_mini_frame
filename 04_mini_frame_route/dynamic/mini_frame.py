#!/usr/bin/env python3
import re
from pymysql import connect


# URL_FUNC_DICT = {
#     "/index.html": index,
#     "/center.html": center
# }

URL_FUNC_DICT = dict()


def route(url):
    def set_func(func):
        # URL_FUNC_DICT["./index.py"] = index
        URL_FUNC_DICT[url] = func

        def call_func(*argv, **kwargv):
            return func(*argv, **kwargv)
        return call_func
    return set_func


@route("/index.html")
def index():
    with open("./templates/index.html") as f:
        content = f.read()

    # 从jing_dong数据库查询所有goods信息
    # 创建connect连接
    # /usr/local/mysql/bin/mysql -u root -p
    option = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "jing_dong",
        "charset": "utf8"
    }
    conn = connect(host=option['host'], port=option['port'], user=option['user'],
                        password=option['password'], database=option['database'],
                        charset=option['charset'])
    # 获得Cursor对象
    cursor = conn.cursor()
    cursor.execute("select * from goods")
    goods_infos = cursor.fetchall()
    cursor.close()
    conn.close()
    html = ""

    for good in goods_infos:
        tr_template = """
            <tr>
              <th scope="row">%s</th>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
            </tr>
            """ % (good[0], good[1], good[2], good[3], good[4])
        html +=  tr_template
    print(html)
    content = re.sub(r"\{%content%\}", html, content)
    return content

@route("/center.html")
def center():
    with open("./templates/center.html") as f:
        content = f.read()
        # 从jing_dong数据库查询所有goods信息
        # 创建connect连接
        # /usr/local/mysql/bin/mysql -u root -p
        option = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "root",
            "database": "jing_dong",
            "charset": "utf8"
        }
        conn = connect(host=option['host'], port=option['port'], user=option['user'],
                       password=option['password'], database=option['database'],
                       charset=option['charset'])
        # 获得Cursor对象
        cursor = conn.cursor()
        cursor.execute("select * from goods")
        goods_infos = cursor.fetchall()
        cursor.close()
        conn.close()
        html = ""

        for good in goods_infos:
            tr_template = """
                <tr>
                  <th scope="row">%s</th>
                  <td>%s</td>
                  <td>%s</td>
                  <td>%s</td>
                  <td>%s</td>
                </tr>
                """ % (good[0], good[1], good[2], good[3], good[4])
            html += tr_template
        print(html)
        content = re.sub(r"\{%content%\}", html, content)
    return content


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    file_name = env['PATH_INFO']

    # if file_name == "/index.py":
    #     return index()
    # elif file_name == "/center.py":
    #     return center()
    # else:
    #     return "hello world 人生苦短 我用python"
    try:
        func = URL_FUNC_DICT[file_name]
        return func()
    except Exception as ret:
        return "产生了异常：%s" % ret

