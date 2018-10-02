import pymysql
import logging

logger = logging.getLogger("myPysql")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler("myPysql.log")
file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

class DBHelper:
    def __init__(self, host="127.0.0.1",
                 user='root',pwd='123456',
                 db='dinping',port=3306,
                 charset='utf8'):
        self.host = host
        self.user = user
        self.port = port
        self.password = pwd
        self.db = db
        self.charset = charset
        self.conn = None#连接
        self.cur = None#游标

    def connectDataBase(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                user=self.user, password=self.password,
                port = self.port,
                db=self.db, charset=self.charset)
        except:
            logger.error("conn Error")
            return False
        self.cur = self.conn.cursor()
        return True

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        return True

    def execute(self, sql, params=None):
        if self.connectDataBase() == False:
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                # 这里的操作可以进行批量化
                self.conn.commit()
        except:
            logger.error("execute"+sql)
            #logger.error("params"+params)
            return False
        return True

    def fetchCount(self, sql, params=None):
        if self.connectDataBase() == False:
            return -1
        self.execute(sql,params)
        return self.cur.fetchone()[0]

if __name__ == '__main__':
    dbhelper = DBHelper()
#    print(dbhelper.connectDataBase())
#    name = "小龙坎老火锅(梅林卓越店)"
#    tel = "0755-88283616"
#    ad  = "+"
#    sql = "INSERT INTO dinping.huoguo(name, tel, ad)VALUES(%s,%s,%s);"
#    params = (name, tel, ad)
#    result = dbhelper.execute(sql, params)
#    if result == True:
#        print("Insert Ok")
#    else:
#        print("Insert Error")

#    print(dbhelper.fetchCount("SELECT * FROM dianping.huoguo"))

    print(dbhelper.close())


logger.removeHandler(file_handler)