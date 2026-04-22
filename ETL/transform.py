import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Parse dates for feature engineering, then serialize back for SQLite.
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    df["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d")
    df["order_date"] = df["order_date"].fillna("")

    # Normalize numeric input columns.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
    df["unit_variable_cost"] = pd.to_numeric(
        df["unit_variable_cost"], errors="coerce"
    ).fillna(0.0)

    # Create time features expected by DB model.
    df["year"] = parsed_dates.dt.year.fillna(0).astype(int)
    df["month"] = parsed_dates.dt.month.fillna(0).astype(int)
    df["quarter"] = parsed_dates.dt.to_period("Q").astype(str).fillna("")

    # Calculate metrics expected by DB model.
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["variable_cost"] = df["quantity"] * df["unit_variable_cost"]
    df["contribution_margin"] = df["revenue"] - df["variable_cost"]
    df["margin_ratio"] = (df["contribution_margin"] / df["revenue"]).where(
        df["revenue"] != 0, 0.0
    )

    return df
