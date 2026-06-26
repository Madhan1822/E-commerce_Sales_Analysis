# E-commerce / Retail Sales Performance Analysis

A portfolio-ready data analyst project: generates a realistic synthetic e-commerce
dataset, loads it into a SQLite database, runs SQL-based RFM segmentation + cohort
analysis, and serves the results in an interactive Streamlit dashboard.

The dataset is fully synthetic (generated with Faker + NumPy), mirroring the schema
of a real-world e-commerce order system — so the project runs end-to-end with no
external downloads, while still demonstrating the same analytical skills as if
working with live data.

---

## 1. Project Structure

```
ecommerce-sales-analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  <- synthetic CSVs get generated here
│   └── processed/            <- cleaned data + sqlite db get saved here
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_rfm_analysis.sql
│   ├── 03_cohort_analysis.sql
│   └── 04_kpi_queries.sql
├── src/
│   ├── generate_sample_data.py   <- generates the synthetic dataset
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

### Step 5 — Generate the sample data
```
python src\generate_sample_data.py
```
This creates realistic synthetic e-commerce data (customers, orders, order items,
products) directly in `data/raw/`. This is the only data source the project uses —
no external download required.

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

## 3. What this project demonstrates (for your resume/portfolio)

- **SQL**: window functions, CTEs, RFM scoring, cohort retention queries (`sql/` folder)
- **Python/Pandas**: synthetic data generation, data cleaning, feature engineering, RFM segmentation logic
- **Data visualization**: interactive Streamlit + Plotly dashboard
- **Business storytelling**: KPI cards (revenue, AOV, repeat-purchase rate), customer
  segment breakdown, and a cohort retention heatmap — the kind of output a real
  e-commerce ops/marketing team would use
  
---

## 4. Next steps to extend it further
- Add a `requirements-dev.txt` with `jupyter` and build an EDA notebook
- Deploy the dashboard for free on Streamlit Community Cloud (great for sharing a live link)
- Add a simple churn-prediction model (logistic regression) using the RFM features
- Swap in a real public dataset (e.g. the Olist Brazilian E-Commerce dataset on Kaggle)
  if you want to validate the pipeline against real-world data later