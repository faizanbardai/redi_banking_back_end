import os
from sqlite3 import Error
import sqlite3
from datetime import datetime, timedelta
import jwt


class Admin:
    def __init__(self):
        self.customers = []
        self.email = None
        self.password = None
        self.authenticated = False

    def login(self, email, password):
        self.email = email
        self.password = password
        adminEmail = os.environ.get("admin-email")
        adminPassword = os.environ.get("admin-password")
        self.authenticated = self.email == adminEmail and self.password == adminPassword
        return self.authenticated

    def get_admin_token(self, secret):
        admin_data = self.get_admin_details()
        admin_data['exp'] = datetime.now() + timedelta(days=2)
        return jwt.encode(admin_data, secret, algorithm='HS256')

    def get_admin_details(self):
        if not self.authenticated:
            return None
        return {
            "email": self.email,
        }

    def is_valid_token(self, token, secret):
        try:
            admin_data = jwt.decode(token, secret, algorithms=['HS256'])
            self.email = admin_data['email']
            self.authenticated = True
            return True

        except(jwt.ExpiredSignatureError, jwt.InvalidSignatureError, ):
            print("Token is not yet valid")
            return False

    def get_all_customers(self):
        if not self.authenticated:
            return None
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            SELECT first_name, last_name, email, address, phone FROM customer
        """
        try:
            cursor.execute(query)
            connection.commit()
            customers = cursor.fetchall()
            keys = ["firstName", "lastName",
                    "email", "address", "phone"]
            customers = [dict(zip(keys, customer)) for customer in customers]
            connection.close()
            for customer in customers:
                self.customers.append(customer)
            return self.customers
        except Error as e:
            print(f"The error '{e}' occurred")
