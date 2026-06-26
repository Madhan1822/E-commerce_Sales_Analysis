# E-commerce / Retail Sales Performance Analysis

A portfolio-ready data analyst project: cleans raw e-commerce order data, loads it into
a SQLite database, runs SQL-based RFM segmentation + cohort analysis, and serves the
results in an interactive Streamlit dashboard.

---

## 1. Project Structure

```
ecommerce-sales-analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  <- put the real Olist CSVs here (optional)
│   └── processed/            <- cleaned data + sqlite db get saved here
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_rfm_analysis.sql
│   ├── 03_cohort_analysis.sql
│   └── 04_kpi_queries.sql
├── src/
│   ├── generate_sample_data.py   <- makes synthetic data so the project runs instantly
│   ├── load_data.py              <- loads CSVs into SQLite
│   ├── clean_data.py             <- cleaning + feature engineering
│   ├── rfm_segmentation.py       <- RFM scoring logic (Python version of the SQL)
│   └── cohort_analysis.py        <- monthly cohort retention matrix
├── dashboard/
│   └── app.py                    <- Streamlit dashboard
└── outputs/                       <- exported charts/reports land here
```

---

## 2. Setup on Windows (step by step)

### Step 1 — Install Python
Download Python 3.11+ from https://www.python.org/downloads/ and during install,
**check "Add Python to PATH"**.

Verify in Command Prompt (cmd) or PowerShell:
```
python --version
```

### Step 2 — Open the project folder
Unzip the project, then in Command Prompt:
```
cd path\to\ecommerce-sales-analysis
```

### Step 3 — Create a virtual environment
```
python -m venv venv
venv\Scripts\activate
```
(You should now see `(venv)` at the start of your prompt line.)

### Step 4 — Install dependencies
```
pip install -r requirements.txt
```

### Step 5 — Generate sample data (so you can run it immediately)
```
python src\generate_sample_data.py
```
This creates realistic synthetic e-commerce data (customers, orders, order items,
products) directly in `data/raw/`, so you don't have to wait on a Kaggle download
to start building.

### Step 6 — Load + clean data into SQLite
```
python src\load_data.py
python src\clean_data.py
```
This produces `data/processed/ecommerce.db`.

### Step 7 — Run the RFM + cohort analysis scripts
```
python src\rfm_segmentation.py
python src\cohort_analysis.py
```
These print summary tables to the console and save CSVs to `outputs/`.

### Step 8 — Launch the dashboard
```
streamlit run dashboard\app.py
```
This opens a browser tab at `http://localhost:8501` with the interactive dashboard.

---

## 3. Switching to the REAL dataset (recommended before showing this to recruiters)

This project is built around the **Olist Brazilian E-Commerce dataset** (100k+ real orders).

1. Go to https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce and download it
   (free Kaggle account required).
2. Extract the CSVs into `data/raw/` — you need at least:
   - `olist_customers_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_order_payments_dataset.csv`
3. Open `src/load_data.py` and set:
   ```python
   USE_SAMPLE_DATA = False
   ```
4. Re-run steps 6–8 above.

---

## 4. What this project demonstrates (for your resume/portfolio)

- **SQL**: window functions, CTEs, RFM scoring, cohort retention queries (`sql/` folder)
- **Python/Pandas**: data cleaning, feature engineering, RFM segmentation logic
- **Data visualization**: interactive Streamlit + Plotly dashboard
- **Business storytelling**: KPI cards (revenue, AOV, repeat-purchase rate), customer
  segment breakdown, and a cohort retention heatmap — the kind of output a real
  e-commerce ops/marketing team would use

### Suggested resume bullet
> "Built an end-to-end e-commerce analytics pipeline (SQL + Python + Streamlit)
> performing RFM customer segmentation and cohort retention analysis on 100K+ orders,
> surfacing actionable insights via an interactive dashboard."

---

## 5. Next steps to extend it further
- Add a `requirements-dev.txt` with `jupyter` and build an EDA notebook
- Deploy the dashboard for free on Streamlit Community Cloud (great for sharing a live link)
- Add a simple churn-prediction model (logistic regression) using the RFM features
