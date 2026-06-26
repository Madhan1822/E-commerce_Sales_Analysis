"""
rfm_segmentation.py
---------------------
Computes Recency, Frequency, Monetary (RFM) scores per customer and assigns
business-friendly segments (Champions, Loyal, At Risk, Lost, etc).

Run: python src/rfm_segmentation.py
"""

import os
import sqlite3

import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def segment_customer(row):
    r, f, m = row["r_score"], row["f_score"], row["m_score"]
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "New Customers"
    if r <= 2 and f >= 3:
        return "At Risk"
    if r <= 2 and f <= 2 and m <= 2:
        return "Lost"
    return "Needs Attention"


def main():
    conn = sqlite3.connect(DB_PATH)
    fact = pd.read_sql(
        "SELECT customer_id, order_purchase_timestamp, order_value FROM order_facts WHERE is_canceled = 0",
        conn,
        parse_dates=["order_purchase_timestamp"],
    )
    conn.close()

    snapshot_date = fact["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = fact.groupby("customer_id").agg(
        recency_days=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_purchase_timestamp", "count"),
        monetary=("order_value", "sum"),
    ).reset_index()

    # Score 1-5 using quantiles (5 = best)
    rfm["r_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    rfm["segment"] = rfm.apply(segment_customer, axis=1)

    segment_summary = (
        rfm.groupby("segment")
        .agg(customers=("customer_id", "count"), avg_monetary=("monetary", "mean"))
        .sort_values("customers", ascending=False)
    )

    print("\n=== RFM Segment Summary ===")
    print(segment_summary.round(2))

    rfm.to_csv(os.path.join(OUTPUT_DIR, "rfm_segments.csv"), index=False)
    print(f"\nSaved full RFM table -> outputs/rfm_segments.csv")
    print("Next step: python src/cohort_analysis.py")


if __name__ == "__main__":
    main()
