"""
向服务端发起请求,展现相应内容
"""


class DictView:
    """
    在线词典查询单词主界面
    """

    def __select_menu1(self):
        """
        一级界面功能菜单
        """
        while True:
            DictView.__display_1()
            meg = input("请输出命令:").strip()
            if meg == "L":
                self.__select_manu2()
            elif meg == "R":
                pass
            elif meg == "q":
                pass
            else:
                print("输入的命令有误,请重新输入!")

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
        self.__select_menu1()


if __name__ == '__main__':
    dict_online = DictView()
    dict_online.main()
