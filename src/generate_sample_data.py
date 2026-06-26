"""
generate_sample_data.py
------------------------
Creates a synthetic but realistic e-commerce dataset (customers, orders,
order_items, products) so the project can be run end-to-end immediately,
without waiting on a Kaggle download.

Mirrors the schema of the Olist Brazilian E-Commerce dataset, so swapping
in the real CSVs later requires no code changes elsewhere.

Run:  python src/generate_sample_data.py
"""

import os
import random
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

N_CUSTOMERS = 2000
N_ORDERS = 8000
N_PRODUCTS = 300
CATEGORIES = [
    "electronics", "home_appliances", "fashion", "beauty", "books",
    "sports", "toys", "furniture", "groceries", "automotive"
]
STATES = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "GO", "PE", "CE"]

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                              seconds=random.randint(0, 86399))


def gen_customers(n):
    rows = []
    for i in range(n):
        rows.append({
            "customer_id": f"CUST{i:06d}",
            "customer_unique_id": str(uuid.uuid4())[:8],
            "customer_city": fake.city(),
            "customer_state": random.choice(STATES),
        })
    return pd.DataFrame(rows)


def gen_products(n):
    rows = []
    for i in range(n):
        category = random.choice(CATEGORIES)
        rows.append({
            "product_id": f"PROD{i:05d}",
            "product_category_name": category,
            "product_weight_g": random.randint(100, 5000),
        })
    return pd.DataFrame(rows)


def gen_orders_and_items(customers_df, products_df, n_orders):
    # Give some customers repeat purchases (for cohort/retention signal),
    # most customers buy 1-2 times, a smaller group buys frequently.
    customer_ids = customers_df["customer_id"].tolist()
    weights = np.random.choice([1, 2, 3, 5, 8], size=len(customer_ids),
                                p=[0.55, 0.25, 0.1, 0.07, 0.03])
    weighted_customer_pool = []
    for cid, w in zip(customer_ids, weights):
        weighted_customer_pool.extend([cid] * w)

    order_rows = []
    item_rows = []
    order_id_counter = 0

    while len(order_rows) < n_orders:
        cid = random.choice(weighted_customer_pool)
        order_id = f"ORD{order_id_counter:07d}"
        order_id_counter += 1

        order_date = random_date(START_DATE, END_DATE)
        status = np.random.choice(
            ["delivered", "delivered", "delivered", "shipped", "canceled"],
            p=[0.78, 0.1, 0.05, 0.05, 0.02]
        )

        order_rows.append({
            "order_id": order_id,
            "customer_id": cid,
            "order_status": status,
            "order_purchase_timestamp": order_date,
        })

        n_items = np.random.choice([1, 2, 3, 4], p=[0.6, 0.25, 0.1, 0.05])
        for _ in range(n_items):
            product = products_df.sample(1).iloc[0]
            price = round(np.random.gamma(shape=2.0, scale=45.0) + 9.9, 2)
            freight = round(price * np.random.uniform(0.03, 0.15), 2)
            item_rows.append({
                "order_id": order_id,
                "order_item_id": str(uuid.uuid4())[:8],
                "product_id": product["product_id"],
                "price": price,
                "freight_value": freight,
            })

    return pd.DataFrame(order_rows), pd.DataFrame(item_rows)


def main():
    print("Generating synthetic e-commerce dataset...")
    customers_df = gen_customers(N_CUSTOMERS)
    products_df = gen_products(N_PRODUCTS)
    orders_df, items_df = gen_orders_and_items(customers_df, products_df, N_ORDERS)

    customers_df.to_csv(os.path.join(RAW_DIR, "olist_customers_dataset.csv"), index=False)
    products_df.to_csv(os.path.join(RAW_DIR, "olist_products_dataset.csv"), index=False)
    orders_df.to_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"), index=False)
    items_df.to_csv(os.path.join(RAW_DIR, "olist_order_items_dataset.csv"), index=False)

    print(f"  customers : {len(customers_df):,} rows -> olist_customers_dataset.csv")
    print(f"  products  : {len(products_df):,} rows -> olist_products_dataset.csv")
    print(f"  orders    : {len(orders_df):,} rows -> olist_orders_dataset.csv")
    print(f"  items     : {len(items_df):,} rows -> olist_order_items_dataset.csv")
    print(f"\nSaved to: {os.path.abspath(RAW_DIR)}")
    print("Next step: python src/load_data.py")


if __name__ == "__main__":
    main()
