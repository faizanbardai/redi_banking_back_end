import sqlite3
from sqlite3 import Error

class Customer:
    def __init__(self, email):
        self.email = email
        self.first_name = None
        self.last_name = None
        self.address = None
        self.phone = None
        self.password = None
    
    def is_new_customer(self):
        return True
    
    def register_customer(self, first_name, last_name, address, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.password = password

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            INSERT INTO customer 
            (email, first_name, last_name, address, phone, password) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (self.email, self.first_name, self.last_name, self.address, self.phone, self.password))
            connection.commit()
            print("New customer added")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def __repr__(self):
        return f"<Customer {self.first_name}>"