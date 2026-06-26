"""
clean_data.py
--------------
Cleans and joins the raw tables into a single analysis-ready 'order_facts' table
saved back into the SQLite database. Handles missing values, dedupes, fixes
dtypes, and adds derived columns (order_value, order_month, etc).

Run: python src/clean_data.py
"""

import os
import sqlite3

import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.db")


def main():
    conn = sqlite3.connect(DB_PATH)

    orders = pd.read_sql("SELECT * FROM orders", conn)
    items = pd.read_sql("SELECT * FROM order_items", conn)
    customers = pd.read_sql("SELECT * FROM customers", conn)
    products = pd.read_sql("SELECT * FROM products", conn)

    # --- Cleaning ---
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    orders = orders.drop_duplicates(subset="order_id")
    items = items.dropna(subset=["price"])
    customers = customers.drop_duplicates(subset="customer_id")

    # Keep only orders that weren't canceled for revenue calcs, but flag it
    orders["is_canceled"] = orders["order_status"].eq("canceled")

    # --- Join into one fact table ---
    item_totals = (
        items.groupby("order_id")
        .agg(order_value=("price", "sum"), freight_total=("freight_value", "sum"), n_items=("order_item_id", "count"))
        .reset_index()
    )

    fact = (
        orders.merge(item_totals, on="order_id", how="left")
        .merge(customers, on="customer_id", how="left")
    )

    fact["order_value"] = fact["order_value"].fillna(0)
    fact["order_month"] = fact["order_purchase_timestamp"].dt.to_period("M").astype(str)
    fact["order_year"] = fact["order_purchase_timestamp"].dt.year

    fact.to_sql("order_facts", conn, if_exists="replace", index=False)
    print(f"  built 'order_facts' table -> {len(fact):,} rows")

    conn.close()
    print("Next step: python src/rfm_segmentation.py")


if __name__ == "__main__":
    main()
