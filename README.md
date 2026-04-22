# Sales Analytics AI App

An interactive sales analytics app built with Streamlit, Pandas, Plotly, and SQLModel.

## What This Project Does

The app lets you upload a sales CSV, transforms and stores it in SQLite, then provides analytics pages for:
- KPI tracking (revenue, margin, margin ratio)
- Quarterly revenue trends
- Quarterly growth rate
- Quarterly average order value
- Top products and product margin analysis
- Revenue comparisons by quarter and category

## How the App Works (End-to-End)

1. **App start** (`app.py`)
- Creates DB tables if they do not exist.
- Shows a CSV uploader.

2. **Validation** (`ETL/validate.py`)
- Checks required columns exist:
  - `order_date`, `product_name`, `category`, `region`, `customer_segment`, `quantity`, `unit_price`, `unit_variable_cost`

3. **Transformation** (`ETL/transform.py`)
- Cleans and normalizes input types.
- Parses `order_date` and derives:
  - `year`, `month`, `quarter`
- Calculates metrics:
  - `revenue = quantity * unit_price`
  - `variable_cost = quantity * unit_variable_cost`
  - `contribution_margin = revenue - variable_cost`
  - `margin_ratio = contribution_margin / revenue` (safe for zero revenue)

4. **Database insert with deduplication** (`Database/crud.py`)
- Inserts transformed rows into `sales.db`.
- Skips duplicates based on these business keys:
  - `order_date`, `product_name`, `category`, `region`, `customer_segment`, `quantity`, `unit_price`, `unit_variable_cost`

5. **Analytics UI pages** (`ui/`)
- **Dashboard** (`ui/dashboard.py`):
  - Filters by `category` and `region`
  - KPI cards
  - Quarterly revenue trend
  - Quarterly growth rate
  - Top products
  - Quarterly average order value
- **Product Analysis** (`ui/product_page.py`):
  - Product revenue table
  - Lowest-margin products
  - Revenue vs margin scatter plot
- **Comparisons** (`ui/comparison_page.py`):
  - Revenue by quarter
  - Revenue by category

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── sales.db
├── Analytics/
│   ├── time_analysis.py
│   ├── growth_rate.py
│   ├── avg_order_value.py
│   └── kpi.py
├── Database/
│   ├── db.py
│   ├── models.py
│   └── crud.py
├── ETL/
│   ├── validate.py
│   ├── transform.py
│   └── ingest.py
├── ui/
│   ├── dashboard.py
│   ├── product_page.py
│   └── comparison_page.py
└── data/
    ├── generate_data.py
    └── sales_data.csv
```

## Data Model

`Database/models.py` defines a `SalesTransaction` table with:
- Input fields: `order_date`, `product_name`, `category`, `region`, `customer_segment`, `quantity`, `unit_price`, `unit_variable_cost`
- Derived fields: `revenue`, `variable_cost`, `contribution_margin`, `margin_ratio`, `year`, `month`, `quarter`

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Upload a CSV

Use your own sales CSV with required columns, or generate sample data.

## Optional: Generate Sample Data

A generator is included at `data/generate_data.py`.

From the project root:

```bash
python data/generate_data.py
```

Then upload the generated CSV file in the Streamlit UI.

## Notes

- Database engine: SQLite (`sales.db`)
- ORM/query layer: SQLModel
- Charts: Plotly Express
- Navigation appears after uploading a file in the current app flow.

## Future Improvements

- Move sidebar navigation outside upload gate so pages can open without re-upload
- Add tests for ETL and dedup logic
- Add authentication and role-based access
- Add forecasting and natural-language query assistant
