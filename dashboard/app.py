"""
dashboard/app.py
------------------
Interactive Streamlit dashboard for the e-commerce sales analysis project.

Run: streamlit run dashboard/app.py
"""

import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

st.set_page_config(page_title="E-commerce Sales Performance", layout="wide")


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    fact = pd.read_sql(
        "SELECT * FROM order_facts WHERE is_canceled = 0",
        conn,
        parse_dates=["order_purchase_timestamp"],
    )
    conn.close()
    return fact


def load_outputs():
    rfm_path = os.path.join(OUTPUT_DIR, "rfm_segments.csv")
    cohort_path = os.path.join(OUTPUT_DIR, "cohort_retention.csv")
    rfm = pd.read_csv(rfm_path) if os.path.exists(rfm_path) else None
    cohort = pd.read_csv(cohort_path, index_col=0) if os.path.exists(cohort_path) else None
    return rfm, cohort


if not os.path.exists(DB_PATH):
    st.error(
        "No database found. Run these first:\n\n"
        "python src/generate_sample_data.py\n"
        "python src/load_data.py\n"
        "python src/clean_data.py"
    )
    st.stop()

fact = load_data()
rfm, cohort = load_outputs()

st.title("📊 E-commerce Sales Performance Dashboard")

# --- Sidebar filters ---
st.sidebar.header("Filters")
states = sorted(fact["customer_state"].dropna().unique())
selected_states = st.sidebar.multiselect("Customer State", states, default=states)

date_min, date_max = fact["order_purchase_timestamp"].min(), fact["order_purchase_timestamp"].max()
date_range = st.sidebar.date_input("Date range", value=(date_min.date(), date_max.date()))

filtered = fact[fact["customer_state"].isin(selected_states)]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["order_purchase_timestamp"].dt.date >= date_range[0])
        & (filtered["order_purchase_timestamp"].dt.date <= date_range[1])
    ]

# --- KPI row ---
total_revenue = filtered["order_value"].sum()
total_orders = filtered["order_id"].nunique()
aov = total_revenue / total_orders if total_orders else 0
repeat_customers = filtered.groupby("customer_id")["order_id"].nunique()
repeat_rate = (repeat_customers > 1).mean() * 100 if len(repeat_customers) else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Avg Order Value", f"R$ {aov:,.2f}")
c4.metric("Repeat Purchase Rate", f"{repeat_rate:.1f}%")

st.divider()

# --- Revenue trend ---
left, right = st.columns(2)

with left:
    st.subheader("Monthly Revenue Trend")
    monthly = filtered.groupby("order_month")["order_value"].sum().reset_index()
    fig = px.line(monthly, x="order_month", y="order_value", markers=True)
    fig.update_layout(yaxis_title="Revenue (R$)", xaxis_title="Month")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by State")
    by_state = filtered.groupby("customer_state")["order_value"].sum().reset_index().sort_values("order_value", ascending=False)
    fig2 = px.bar(by_state, x="customer_state", y="order_value")
    fig2.update_layout(yaxis_title="Revenue (R$)", xaxis_title="State")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- RFM segmentation ---
st.subheader("Customer Segments (RFM)")
if rfm is not None:
    seg_summary = rfm.groupby("segment").agg(
        customers=("customer_id", "count"), avg_monetary=("monetary", "mean")
    ).reset_index().sort_values("customers", ascending=False)

    col1, col2 = st.columns([1, 1])
    with col1:
        fig3 = px.pie(seg_summary, names="segment", values="customers", title="Customers per Segment")
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.dataframe(seg_summary.round(2), use_container_width=True)
else:
    st.info("Run `python src/rfm_segmentation.py` to generate segment data.")

st.divider()

# --- Cohort retention ---
st.subheader("Monthly Cohort Retention (%)")
if cohort is not None:
    st.dataframe(
        cohort.iloc[:, :6].style.background_gradient(cmap="Blues", axis=None).format("{:.1f}"),
        use_container_width=True,
    )
else:
    st.info("Run `python src/cohort_analysis.py` to generate cohort data.")

st.caption("Data source: synthetic sample data mirroring the Olist Brazilian E-Commerce dataset schema. Swap in real data per README section 3.")
