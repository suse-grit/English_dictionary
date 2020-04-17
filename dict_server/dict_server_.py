"""
接收客户端请求,进行处理
"""
# 导入相应模块
from socket import *
from dict_server.dict_server_db import *
from multiprocessing import *
import signal
import sys

# 定义全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)


class DictServer(Process):
    """
    自定义进程类,处理客户端请求
    """

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        pass


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
