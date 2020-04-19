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
                # 如果登录成功则进入二级界面
                name = self.__login()
                if name:
                    self.__select_manu2(name)
            elif meg == "R":
                self.__register()
            elif meg == "q":
                self.__client.send(b"q")
                sys.exit("客户端退出!")
            else:
                print("输入的命令有误,请重新输入!")

    def __login(self):
        """
        客户端登录处理
        """
        while True:
            name = input("请输入你的用户名:")
            password = input("请输入你的密码(大于6位数):")
            if len(password) < 6:
                print("密码位数不够,请重新操作!")
                continue
            elif (" " in name) or (" " in password):
                print("用户名与密码中有空格存在,请重新操作!")
                continue
            data = "L " + name + " " + password
            self.__client.send(data.encode())
            meg = self.__client.recv(1024).decode()
            if not meg:
                sys.exit("服务器无响应!")
            elif meg == "YES":
                print("登录成功!")
                return name
            else:
                print("用户名不存在或密码错误,登录失败!")
                return False

    def __register(self):
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
            self.__client.send(data.encode())
            meg = self.__client.recv(1024).decode()
            if not meg:
                sys.exit("服务器无响应!")
            elif meg == "YES":
                print("注册成功!")
            else:
                print("用户已存在,注册失败!")
            return

    def __query(self, name):
        """
        处理客户端单词查询
        """
        while True:
            word = input("请输入你想要查询的单词(输入'##'可以退出查询):").strip()
            if word == "##":
                break
            if not word:
                print("输入的单词为空,请重新输入!")
                continue
            data = "Q %s %s" % (name, word)
            self.__client.send(data.encode())
            # 如果查到单词则返回解释, 如果没有查到, 无论什么结果都打印
            result = self.__client.recv(1024).decode()
            print(result)

    def __history(self, name):
        """
        查看单词查询的历史记录
        :param name: 查询历史记录的用户名
        """
        data = "H " + name
        self.__client.send(data.encode())
        while True:
            meg = self.__client.recv(1024).decode()
            if meg == "##":
                break
            print(meg)

    def __select_manu2(self, name):
        """
        二级界面功能菜单
        """
        while True:
            self.__display_2()
            meg = input("请输出命令:").strip()
            if meg == "Q":
                self.__query(name)
            elif meg == "H":
                self.__history(name)
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
        print("""===========   欢迎进入查询界面   ============
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
