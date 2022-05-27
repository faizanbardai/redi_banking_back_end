import os
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from classes.customer import Customer
from dotenv import load_dotenv

from db.database import Database

load_dotenv()
origins = [os.environ.get("front-end")]
print(os.environ.get("front-end"))

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
    return {"message": "Hello World"}


class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str
    email: str
    password: str


@app.post("/customer/register", status_code=status.HTTP_201_CREATED)
async def create_customer(user: RegisterUser, response: Response):
    customer = Customer(user.email)
    if customer.is_new_customer():
        customer.register_customer(
            user.first_name, user.last_name, user.address, user.phone, user.password)
        return {"message": "Your account is successfully created."}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Your email is already registered."}


class LoginUser(BaseModel):
    email: str
    password: str


@app.post("/customer/login", status_code=status.HTTP_200_OK)
async def login_customer(user: LoginUser, response: Response):
    customer = Customer(user.email)
    if customer.login_customer(user.password):
        return {"message": "You are successfully logged in."}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid credentials."}
