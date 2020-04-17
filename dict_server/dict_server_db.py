"""
与服务端进行数据库交互
"""
from pymysql import *


# 创建一个数据库类,实现与服务端处理逻辑进行数据交互
class Database:
    def __init__(self):
        # 创建一个数据库对象
        self.db = connect(host="127.0.0.1",
                          port=3306,
                          user="root",
                          password="123456",
                          database="dict",
                          charset="utf8")
        # 创建一个游标对象,操作数据库
        self.cur = self.db.cursor()

    def close(self):
        """
        关闭数据库游标对象与数据库
        """
        self.cur.close()
        self.db.close()

    def find_word(self):
        pass

    def login(self):
        pass

    def find_history(self):
        pass
