import pymysql
class DBconnector:
    def __init__(self, schema):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.port = 3306
        self.password = 'ScE1234**'
        self.db = schema

    def __connect__(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    passwd=self.password,
                                    charset='utf8mb4',
                                    db=self.db)
        self.cur = self.conn.cursor()

    def __disconnect__(self):
        self.conn.close()

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()

    def fetch_all(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result =self.cur.fetchall()
        self.__disconnect__()
        return result

    def fetch_one(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.__disconnect__()
        return result[0]

    def save(self, sql):
        self.__connect__()
        result = self.cur.execute(sql)
        self.conn.commit()
        self.__disconnect__()
        return result

    def update(self, sql):
        self.__connect__()
        result = self.cur.execute(sql)
        self.conn.commit()
        self.__disconnect__()
        return result

    def insert(self, sql):
        self.__connect__()
        result = self.cur.execute(sql)
        self.conn.commit()
        self.__disconnect__()
        return result

    def delete(self, sql):
        self.__connect__()
        result = self.cur.execute(sql)
        self.conn.commit()
        self.__disconnect__()