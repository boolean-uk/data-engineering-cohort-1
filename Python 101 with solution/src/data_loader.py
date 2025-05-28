import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data"

def load_data():
    customers = pd.read_csv(DATA_PATH / "customers.csv", parse_dates=["signup_date"])
    orders = pd.read_csv(DATA_PATH / "orders.csv", parse_dates=["order_date"])
    return customers, orders

def get_customer_aggregates():
    customers, orders = load_data()
    df = customers.merge(orders, on='customer_id', how='left')  # LEFT join ensures all customers included
    agg = df.groupby(['customer_id', 'name'], as_index=False).agg(
        total_spent=('amount', 'sum')
    )
    agg['total_spent'] = agg['total_spent'].fillna(0.0)
    return agg

def get_customer_by_id(customer_id: int):
    agg = get_customer_aggregates()
    customer = agg[agg['customer_id'] == customer_id]
    return None if customer.empty else customer.iloc[0].to_dict()