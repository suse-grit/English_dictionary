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

    def create_cur(self):
        """
        创建游标对象
        """
        self.cur = self.db.cursor()

    def close(self):
        """
        关闭数据库游标对象与数据库
        """
        self.cur.close()
        self.db.close()

    def register(self, name, password):
        """
        数据库处理注册请求
        :param name: 注册用户名
        :param password: 注册密码
        :return: 注册成功:True  注册失败:False
        """
        sql = "select name from user where name=%s"
        self.cur.execute(sql, [name])
        if self.cur.fetchone():
            return False
        else:
            sql = "insert into user(name,passwd) values(%s,%s) "
            self.cur.execute(sql, [name, password])
            self.db.commit()
            return True

    def login(self, name, password):
        sql = "select name from user where name=%s and passwd=%s;"
        self.cur.execute(sql, [name, password])
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def find_history(self):
        pass
