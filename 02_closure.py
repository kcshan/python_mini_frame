# 初中学过函数，例如 y = 1*x + 2*y + 3*c
# 计算 y = k*x + b


def line_2(k, b, x):
    print(k*x + b)

line_2(1, 2, 1)
line_2(1, 2, 2)
line_2(1, 2, 3)

print('-------')


def line_3(x, k=1, b=2):
    print(k*x + b)
line_3(0)
line_3(1)
line_3(2)

line_3(1, k=11, b=0)
line_3(1, k=22, b=0)
line_3(1, k=33, b=0)

print('-------')

class Line4(object):
    def __init__(self, k, b):
        self.k = k
        self.b = b

    def __call__(self, x):
        print(self.k * x + self.b)

line_4_1 = Line4(1, 2)
line_4_1(0)
line_4_1(1)
line_4_1(2)

line_4_2 = Line4(11, 22)
line_4_2(0)
line_4_2(1)
line_4_2(2)

print('-------')

def line_5(k, b):
    def create(x):
        print(k * x + b)
    return create

line_5_1 = line_5(1, 2)
line_5_1(0)
line_5_1(1)
line_5_1(2)

print('-------')

x = 300
def test1():
    x = 200
    def test2():
        nonlocal x
        print("---1---x=%d" % x)
        x = 100
        print("---2---x=%d" % x)
    return test2

t1 = test1()
t1()

