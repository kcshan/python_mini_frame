def index():
    with open("./templates/index.html") as f:
        return f.read()


def center():
    with open("./templates/center.html") as f:
        return f.read()


def application(env, start_response):
    print(123)
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    file_name = env['PATH_INFO']

    if file_name == "/index.py":
        return index()
    elif file_name == "/center.py":
        return center()
    else:
        return "hello world 人生苦短 我用python"

