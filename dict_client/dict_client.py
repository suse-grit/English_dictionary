"""
向服务端发起请求,展现相应内容
"""
from socket import *
import sys

ADDR = ("127.0.0.1", 8888)


class DictView:
    """
    在线词典查询单词主界面
    """

    def __init__(self, client):
        self.client = client

    def __select_menu1(self):
        """
        一级界面功能菜单
        """
        while True:
            DictView.__display_1()
            meg = input("请输出命令:").strip()
            if meg == "L":
                self.login()
            elif meg == "R":
                self.register()
            elif meg == "q":
                pass
            else:
                print("输入的命令有误,请重新输入!")

    def login(self):
        """
        客户端登录处理
        """
        while True:
            name = input("请输入你的用户名:")
            password = input("请输入你的密码(大于6位数):")
            if len(password) < 6:
                print("密码位数不够,请重新操作()!")
                continue
            elif (" " in name) or (" " in password):
                print("用户名与密码中有空格存在,请重新操作!")
                continue
            data = "L " + name + " " + password
            self.client.send(data.encode())
            meg = self.client.recv(1024).decode()
            if not meg:
                sys.exit("服务器无响应!")
            elif meg == "YES":
                print("登录成功!")
            else:
                print("用户不存在,登录失败!")
            return

    def register(self):
        """
        客户端注册处理
        """
        while True:
            name = input("请输入用户名:")
            password = input("请输入注册密码(大于6位数):")
            if len(password) < 6:
                print("密码位数不够,请重新操作()!")
                continue
            elif (" " in name) or (" " in password):
                print("用户名与密码中有空格存在,请重新操作!")
                continue
            data = "R " + name + " " + password
            self.client.send(data.encode())
            meg = self.client.recv(1024).decode()
            if not meg:
                sys.exit("服务器无响应!")
            elif meg == "YES":
                print("注册成功!")
            else:
                print("注册失败!")
            return

    def __select_manu2(self):
        """
        二级界面功能菜单
        """
        self.__display_2()
        while True:
            meg = input("请输出命令:").strip()
            if meg == "Q":
                pass
            elif meg == "H":
                pass
            elif meg == "E":
                break
            else:
                print("输入的命令有误,请重新输入!")

    @staticmethod
    def __display_1():
        """
        一级界面提示信息
        """
        print("""
        *******   登录-->L   *******
        *******   注册-->R   *******
        *******   退出-->q   *******
        """)

    @staticmethod
    def __display_2():
        """
        二级界面提示信息
        """
        print("""
        *******   查单词-->Q   *******
        *******   历史记录-->H  *******
        *******   注销-->E      ******
        """)

    def main(self):
        print("""
        ************  欢迎进入在线字典查询界面  ***********
        """)
        self.__select_menu1()


def main():
    client = socket(AF_INET, SOCK_STREAM)
    try:
        client.connect(ADDR)
        dict_ciew = DictView(client)
        while True:
            dict_ciew.main()
    except KeyboardInterrupt:
        sys.exit("客户端退出!")
    except Exception as e:
        print(e)
        sys.exit("客户端退出!")


if __name__ == '__main__':
    main()
