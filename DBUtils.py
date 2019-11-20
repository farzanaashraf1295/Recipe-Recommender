import pymysql

HOST = "localhost"
USERNAME = "root"
PASSWORD = "mysql"
DATABASE = "recipemaker"


class DBUtils:
    _instance = None

    @staticmethod
    def get_instance():
        if not DBUtils._instance:
            DBUtils._instance = DBUtils()
        return DBUtils._instance

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)

    def close(self):
        if self.connection.open:
            self.connection.close()

    def insert(self, sql, args):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql, args)
                self.connection.commit()
                self.close()
                return cursor.lastrowid
        except Exception as ex:
            print(ex)
            self.close()
        return 0

    def get(self, sql):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                columns = [t[0] for t in cursor.description]
                if results:
                    results = list(map(lambda x: {k: v for k, v in zip(columns, x)}, results))
                self.close()
                return results
        except Exception as ex:
            print(ex)
            self.close()
        return None

    def update(self, sql, args):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql, args)
                self.connection.commit()
                self.close()
        except Exception as ex:
            print(ex)
            self.close()
        return None

    def delete(self, sql):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                self.close()
        except Exception as ex:
            print(ex)
            self.close()
        return None
