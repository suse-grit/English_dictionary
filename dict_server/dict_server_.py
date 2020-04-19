"""
接收客户端请求,进行处理
"""
# 导入相应模块
from socket import *
from dict_server.dict_server_db import *
from multiprocessing import *
from time import sleep
import signal
import sys, os

# 定义全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

# 建立与数据库的连接
db = Database()


class DictServer(Process):
    """
    自定义进程类,处理客户端请求
    """

    def __init__(self, client):
        super().__init__()
        self.client = client

    # 总分模式:一个地方负责接受请求,根据请求类型进行任务分发
    def run(self):
        db.create_cur()  # 每个子进程都创建自己的游标对象
        while True:
            data = self.client.recv(1024).decode()
            meg = data.split()
            if not meg or data == "q":
                self.client.close()
                db.close()
                os._exit(0)
            elif meg[0] == "R":
                self.do_register(meg[1], meg[2])
            elif meg[0] == "L":
                self.do_login(meg[1], meg[2])
            elif meg[0] == "Q":
                self.do_query(meg[1], meg[2])
            elif meg[0] == "H":
                self.do_history(meg[1])

    def do_history(self, name):
        """
        处理客户端历史记录查询请求
        :param name: 客户端用户名
        """
        result = db.history(name)
        for name, word, time in result:
            data = "用户:{} 在{} 查询了单词:{}".format(name, time, word)
            self.client.send(data.encode())
            sleep(0.1)
        self.client.send(b"##")

    def do_login(self, name, password):
        """
        处理客户端登录请求
        :param name: 请求登录的用户名
        :param password: 请求登录的用户名密码
        """
        if db.login(name, password):
            self.client.send(b"YES")
        else:
            self.client.send(b"NO")

    def do_register(self, name, password):
        """
        处理客户端注册请求
        :param name: 请求注册的用户名
        :param password: 请求注册的用户密码
        """
        if db.register(name, password):
            self.client.send(b"YES")
        else:
            self.client.send(b"NO")

    def do_query(self, name, word):
        """
        处理客户端单词查询请求
        :param name: 客户端用户名
        :param word: 客户端想要查询的单词
        """
        mean = db.query(name, word)
        if mean:
            data = "{} : {}".format(word, mean)
        else:
            data = "单词:{} 未找到!".format(word)
        self.client.send(data.encode())


def main():
    """
    搭建主函数
    """
    # 创建tcp监听套接字
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)
    # 设置监听套接字关闭后地址重用
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 0)
    # 设置信号量,子进程退出后系统回收,防止产生僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 循环等待客户端连接,采用多进程处理客户端连接
    while True:
        try:
            con_fd, addr = server_socket.accept()
            print("connect from:", addr)
        except KeyboardInterrupt:
            sys.exit("服务器退出!")
        except Exception as e:
            print(e)
            continue
            # 实例化自定义的多进程类(继承于Process类)
        p = DictServer(con_fd)
        p.daemon = True  # 设置主进程退出时,子进程都退出
        p.start()


if __name__ == '__main__':
    main()
