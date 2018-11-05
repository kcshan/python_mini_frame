import time


def set_func(func):
    def call_func(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        print("func_time: %f" % (start_time - stop_time))
    return call_func


@set_func
def t_func():
    print("---test_1---")

t_func()


def set_func_1(func):
    def call_func(*args, **kwargs):
        return "<h1>" + func(*args, **kwargs) + "</h1>"
    return call_func


def set_func_2(func):
    def call_func(*args, **kwargs):
        return "<div>" + func(*args, **kwargs) + "</div>"
    return call_func


@set_func_1
@set_func_2
def t_func_1():
    return "haha"

print(t_func_1())


class SetFunc():
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return "<h1>" + self.func() + "</h1>"


@SetFunc
def t_func_2():
    return "haha"

print(t_func_2())


def set_level(level_num):
    def set_func_3(func):
        def call_func(*args, **kwargs):
            if level_num == 1:
                print("---验证权限1---")
            elif level_num == 2:
                print("---验证权限2---")
            func()
        return call_func
    return set_func_3

@set_level(1)
def t_func_3():
    print("---test_1---")


@set_level(2)
def t_func_4():
    print("---test_2---")

t_func_3()
t_func_4()