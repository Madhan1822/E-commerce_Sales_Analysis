"""
cohort_analysis.py
---------------------
Builds a monthly cohort retention matrix: for each customer's first-purchase
month (cohort), what % of those customers came back in month 1, 2, 3... after.

Run: python src/cohort_analysis.py
"""

import os
import sqlite3

import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    conn = sqlite3.connect(DB_PATH)
    fact = pd.read_sql(
        "SELECT customer_id, order_purchase_timestamp FROM order_facts WHERE is_canceled = 0",
        conn,
        parse_dates=["order_purchase_timestamp"],
    )
    conn.close()

    fact["order_month"] = fact["order_purchase_timestamp"].values.astype("datetime64[M]")
    cohort_month = fact.groupby("customer_id")["order_month"].min().rename("cohort_month")
    fact = fact.join(cohort_month, on="customer_id")

    fact["cohort_index"] = (
        (fact["order_month"].dt.year - fact["cohort_month"].dt.year) * 12
        + (fact["order_month"].dt.month - fact["cohort_month"].dt.month)
    )

    cohort_data = (
        fact.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique()
        .reset_index()
    )

    cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0).round(3) * 100

    print("\n=== Monthly Cohort Retention (%) ===")
    print(retention.iloc[:, :6].round(1))  # first 6 months for readability

    retention.to_csv(os.path.join(OUTPUT_DIR, "cohort_retention.csv"))
    print(f"\nSaved full retention matrix -> outputs/cohort_retention.csv")
    print("Next step: streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()
