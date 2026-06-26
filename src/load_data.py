"""
load_data.py
-------------
Loads raw CSVs from data/raw/ into a SQLite database at data/processed/ecommerce.db.

Set USE_SAMPLE_DATA = False once you've downloaded the real Olist dataset into
data/raw/ (see README section 3).

Run: python src/load_data.py
"""

import os
import sqlite3

import pandas as pd

USE_SAMPLE_DATA = True  # flip to False after adding real Olist CSVs to data/raw/

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(PROCESSED_DIR, "ecommerce.db")

os.makedirs(PROCESSED_DIR, exist_ok=True)

FILES = {
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
}


def main():
    if not os.path.exists(os.path.join(RAW_DIR, FILES["orders"])):
        raise FileNotFoundError(
            "No raw data found. Run 'python src/generate_sample_data.py' first, "
            "or add the real Olist CSVs to data/raw/."
        )

    conn = sqlite3.connect(DB_PATH)

    for table_name, filename in FILES.items():
        path = os.path.join(RAW_DIR, filename)
        df = pd.read_csv(path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"  loaded {len(df):,} rows -> table '{table_name}'")

    conn.close()
    print(f"\nDatabase ready at: {os.path.abspath(DB_PATH)}")
    print("Next step: python src/clean_data.py")


if __name__ == "__main__":
    main()
