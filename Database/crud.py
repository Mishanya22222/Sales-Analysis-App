from sqlmodel import Session, select
import pandas as pd
from Database.models import SalesTransaction


DB_COLUMNS = [
    "order_date",
    "product_name",
    "category",
    "region",
    "customer_segment",
    "quantity",
    "unit_price",
    "unit_variable_cost",
    "revenue",
    "variable_cost",
    "contribution_margin",
    "margin_ratio",
    "year",
    "month",
    "quarter",
]

FLOAT_COLUMNS = {
    "unit_price",
    "unit_variable_cost",
    "revenue",
    "variable_cost",
    "contribution_margin",
    "margin_ratio",
}
INT_COLUMNS = {"quantity", "year", "month"}
DEDUP_COLUMNS = [
    "order_date",
    "product_name",
    "category",
    "region",
    "customer_segment",
    "quantity",
    "unit_price",
    "unit_variable_cost",
]


def insert_dataframe(session: Session, df):
    prepared_df = df.copy()
    if "order_date" in prepared_df.columns:
        prepared_df["order_date"] = (
            pd.to_datetime(prepared_df["order_date"], errors="coerce")
            .dt.strftime("%Y-%m-%d")
            .fillna("")
        )

    for col in DB_COLUMNS:
        if col not in prepared_df.columns:
            if col in FLOAT_COLUMNS:
                prepared_df[col] = 0.0
            elif col in INT_COLUMNS:
                prepared_df[col] = 0
            else:
                prepared_df[col] = ""

    records = prepared_df[DB_COLUMNS].to_dict(orient="records")

    existing_rows = session.exec(
        select(*[getattr(SalesTransaction, col) for col in DEDUP_COLUMNS])
    ).all()
    existing_keys = {tuple(row) for row in existing_rows}

    new_records = []
    seen_upload_keys = set()
    for record in records:
        record_key = tuple(record[col] for col in DEDUP_COLUMNS)
        if record_key in existing_keys or record_key in seen_upload_keys:
            continue
        seen_upload_keys.add(record_key)
        new_records.append(record)

    if not new_records:
        return 0, len(records)

    objects = [SalesTransaction(**record) for record in new_records]
    session.add_all(objects)
    session.commit()
    return len(new_records), len(records) - len(new_records)
