from fastapi import FastAPI

from db.database import Database
from db.queries.create_customer_table import create_customer_table_query

app = FastAPI()

database = Database()
database.create_connection()
database.create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}