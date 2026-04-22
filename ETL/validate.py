def validate_columns(df):
    required = [
        "order_date",
        "product_name",
        "category",
        "region",
        "customer_segment",
        "quantity",
        "unit_price",
        "unit_variable_cost"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        return False, f"Missing columns: {missing}"

    return True, "Valid dataset"
