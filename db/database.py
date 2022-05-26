import sqlite3
from sqlite3 import Error
from db.queries.create_customer_table import create_customer_table_query

class Database:
    _path = "./database.db"
    _connection = None

    def __init__(self):
        pass

    def create_connection(self):
        try:
            self._connection = sqlite3.connect(self._path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
    

    def execute_query(self,query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_tables(self):
        self.execute_query(create_customer_table_query)