from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Customer(BaseModel):
    id: int
    name: str
    total_spent: float

@app.get("/")
def root():
    return {"message": "Welcome to the Data API"}

@app.get("/customers/top")
def top_customers():
    return [
        {"id": 102, "name": "Bob", "total_spent": 320},
        {"id": 101, "name": "Alice", "total_spent": 300},
        {"id": 103, "name": "Charlie", "total_spent": 130}
    ]

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    if customer_id == 101:
        return {"name": "Alice", "total_spent": 300}
    return {"error": "Customer not found"}
