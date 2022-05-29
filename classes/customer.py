from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error

import jwt


class Customer:

    def __init__(self, email):
        self.email = email
        self.first_name = None
        self.last_name = None
        self.address = None
        self.phone = None
        self.password = None

    def is_new_customer(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            SELECT * FROM customer WHERE email = ?
        """
        try:
            cursor.execute(query, (self.email,))
            result = cursor.fetchone()
            connection.close()
            return False if result else True
        except Error as e:
            print(f"The error '{e}' occurred")

    def login_customer(self, password):
        self.password = password
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            SELECT * FROM customer WHERE email = ? AND password = ?
        """
        try:
            cursor.execute(query, (self.email, self.password))
            result = cursor.fetchone()
            connection.close()
            if result:
                self.first_name = result[1]
                self.last_name = result[2]
                self.address = result[3]
                self.phone = result[4]
                return True
            else:
                return False
        except Error as e:
            print(f"The error '{e}' occurred")

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
            cursor.execute(query, (self.email, self.first_name,
                           self.last_name, self.address, self.phone, self.password))
            connection.commit()
            connection.close()
            print("New customer added")
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_customer_details(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }

    def get_customer_token(self, secret):
        customer_data = self.get_customer_details()
        customer_data['exp'] = datetime.now() + timedelta(seconds=20)
        return jwt.encode(customer_data, secret, algorithm='HS256')

    def is_valid_token(self, token, secret):
        try:
            jwt.decode(token, secret, algorithms=['HS256'])
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    def set_customer_data_from_token(self, token, secret):
        customer_data = jwt.decode(token, secret, algorithms=['HS256'])
        self.first_name = customer_data['firstName']
        self.last_name = customer_data['lastName']
        self.address = customer_data['address']
        self.phone = customer_data['phone']
        self.email = customer_data['email']

        return self.get_customer_details()

    def __repr__(self):
        return f"<Customer {self.first_name}>"
