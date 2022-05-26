import os
from fastapi import FastAPI
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

class User(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str
    email: str
    password: str

@app.post("/customer")
async def create_customer(user: User):
    customer = Customer(user.email)
    if(customer.is_new_customer):
        customer.register_customer(user.first_name, user.last_name, user.address, user.phone, user.password)
    else:
        print("Old customer")

    return {"message": "Customer created"}