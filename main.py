import os
from typing import Union
from fastapi import FastAPI, Response, status, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from classes.bank_account import BankAccount
from classes.customer import Customer
from dotenv import load_dotenv

from db.database import Database

load_dotenv()
origins = [os.environ.get("front-end")]

secret = os.environ.get("jwt-secret")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database()
database.create_connection()
database.create_tables()


@app.get("/")
async def root():
    return {"message": "Welcome to my banking app!"}


class User(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    address: Union[str, None] = None
    phone: Union[str, None] = None
    email: str
    password: str


@app.post("/customer/register", status_code=status.HTTP_201_CREATED)
async def create_customer(user: User, response: Response):
    customer = Customer(user.email)
    if customer.is_new_customer():
        customer.register_customer(
            user.first_name, user.last_name, user.address, user.phone, user.password)

        return {
            "message": "Your account is successfully created.",
            "customer": customer.get_customer_details(),
            "token": customer.get_customer_token(secret)
        }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Your email is already registered."}


@app.post("/customer/login", status_code=status.HTTP_200_OK)
async def login_customer(user: User, response: Response):
    customer = Customer(user.email)
    if customer.login_customer(user.password):
        return {
            "message": "You are successfully logged in.",
            "customer": customer.get_customer_details(),
            "token": customer.get_customer_token(secret)
        }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid credentials."}


@app.get("/customer/data", status_code=status.HTTP_200_OK)
async def get_customer_data(response: Response, token: str = Header(None)):
    customer = Customer('')
    if customer.is_valid_token(token, secret):
        return {
            "message": "You are successfully logged in.",
            "customer": customer.get_customer_details()
        }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token."}


class Account(BaseModel):
    type: str
    name: str
    number: Union[str, None] = None
    amount: Union[float, None] = None


@app.post("/customer/create-bank-account", status_code=status.HTTP_201_CREATED)
async def create_bank_account(account: Account, response: Response, token: str = Header(None)):
    customer = Customer('')
    if customer.is_valid_token(token, secret):
        account_details = customer.create_bank_account(
            account.type, account.name)
        return {
            "message": "Your bank account is successfully created.",
            "bankAccount": account_details
        }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token."}


@app.post("/customer/deposit", status_code=status.HTTP_201_CREATED)
async def deposit_money(account: Account, response: Response, token: str = Header(None)):
    customer = Customer('')
    if customer.is_valid_token(token, secret):
        bank_account = BankAccount(customer.email)
        if bank_account.is_valid_account(account.number):
            bank_account.deposit(account.amount)
            return {
                "message": "You have successfully deposited money.",
                "bankAccount": bank_account.get_account_details()
            }
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Invalid bank account number"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token."}


@app.post("/customer/withdraw", status_code=status.HTTP_201_CREATED)
async def withdraw_money(account: Account, response: Response, token: str = Header(None)):
    customer = Customer('')
    if customer.is_valid_token(token, secret):
        bank_account = BankAccount(customer.email)
        if bank_account.is_valid_account(account.number):
            try:
                bank_account.withdraw(account.amount)
            except ValueError as err:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"message": str(err)}
            return {
                "message": "You have successfully withdrawn money.",
                "bankAccount": bank_account.get_account_details()
            }
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Invalid bank account number"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token."}


@app.get("/customer/bank-accounts", status_code=status.HTTP_201_CREATED)
async def get_bank_accounts(response: Response, token: str = Header(None)):
    customer = Customer('')
    if customer.is_valid_token(token, secret):
        return {
            "message": "You have successfully retrieved your bank accounts.",
            "bankAccounts": customer.get_bank_accounts()
        }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid token."}
