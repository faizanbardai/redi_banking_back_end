import sqlite3
from sqlite3 import Error
import uuid


class BankAccount:
    def __init__(self, email):
        self.email = email
        self.name = None
        self.number = None
        self.type = None
        self.balance = 0

    def create_bank_account(self, type, name):
        self.type = type
        self.name = name
        self.number = str(uuid.uuid4())
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            INSERT INTO bank_account (number, type, name, balance, email)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (self.number,
                           self.type, name, self.balance, self.email))
            connection.commit()
            connection.close()
            return True
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    def deposit(self, amount):
        self.balance += amount
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            UPDATE bank_account SET balance = ? WHERE number = ?
        """
        try:
            cursor.execute(query, (self.balance, self.number))
            connection.commit()
            connection.close()
        except Error as e:
            print(f"The error '{e}' occurred")

    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            UPDATE bank_account SET balance = ? WHERE number = ?
        """
        try:
            cursor.execute(query, (self.balance, self.number))
            connection.commit()
            connection.close()
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_balance(self):
        return self.balance

    def is_valid_account(self, number):
        self.number = number
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = """
            SELECT * FROM bank_account WHERE number = ?
        """
        try:
            cursor.execute(query, (self.number,))
            result = cursor.fetchone()
            connection.close()
            if result:
                self.email = result[0]
                self.type = result[2]
                self.name = result[3]
                self.balance = result[4]

                return True
            else:
                return False
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_account_details(self):
        return {
            "number": self.number,
            "type": self.type,
            "balance": self.balance,
            "name": self.name,
            "email": self.email
        }
