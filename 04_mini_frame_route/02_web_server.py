import socket
import re
import multiprocessing


class WSGIServer(object):
    def __init__(self):
        # 1. 创建套接字
        # self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close 即服务器4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时，可以立即启动
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2. 绑定
        self.tcp_server_socket.bind(("", 7890))

        # 3. 监听套接字
        self.tcp_server_socket.listen(128)

    def service_client(self, new_socket):
        """为这个客户端返回数据"""
        # 1. 接收浏览器发送过来的请求，即http请求
        # GET /HTTP/1.1
        # ......
        request = new_socket.recv(1024).decode("utf-8")
        # print("-" * 50)
        # print(request)

        request_lines = request.splitlines()
        print("")
        print(">>>" * 20)
        print(request_lines)

        # GET /index.html HTTP/1.1
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        file_name = ""
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"
            print("*" * 50, file_name)

        # 2. 返回http格式的数据，给浏览器
        # 2.1 如果请求的资源不是以.py结尾，那么就认为是静态资源（html/css/js/png, jpg等）
        if not file_name.endswith(".py"):
            try:
                # f = open("./html/index.html", "rb")
                f = open("./html" + file_name, "rb")
            except:
                # header
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                # body
                response += "----file not found----"
                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))

            else:
                # header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # body
                html_content = f.read()
                f.close()
                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)
        else:
            # 2.2 如果是以.py结尾，那么就认为是动态资源的请求
            header = "HTTP/1.1 200 OK\r\n"
            header += "\r\n"
            body = "hahaha"
            response = header + body
            new_socket.send(response.encode("utf-8"))

        # 关闭套接字
        new_socket.close()


    def run_forever(self):
        """用来完成整体的控制"""


        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()

            # 5. 为这个客户端服务
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            p.start()
            new_socket.close()

        # 6. 关闭监听套接字
        self.tcp_server_socket.close()


def main():
    """控制整体，创建一个web服务器对象，然后调用这个对象的run_forever方法运行"""
    wsgi_server = WSGIServer()
    wsgi_server.run_forever()


if __name__ == "__main__":
    main()
