from fastapi import FastAPI
from pydantic import BaseModel
from src.data_loader import get_customer_aggregates, get_customer_by_id

app = FastAPI()

class Customer(BaseModel):
    id: int
    name: str
    total_spent: float

@app.get("/")
def root():
    return {"message": "Welcome to the Data API"}

@app.get("/customers/top", response_model=list[Customer])
def top_customers():
    df = get_customer_aggregates()
    df = df.sort_values(by='total_spent', ascending=False).head(3)
    return [
        Customer(id=row['customer_id'], name=row['name'], total_spent=row['total_spent'])
        for _, row in df.iterrows()
    ]

@app.get("/customer/{customer_id}", response_model=Customer | dict)
def get_customer(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if customer:
        return Customer(id=customer['customer_id'], name=customer['name'], total_spent=customer['total_spent'])
    return {"error": "Customer not found"}
