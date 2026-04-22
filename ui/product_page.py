import streamlit as st
import pandas as pd
import plotly.express as px

from Database.db import get_session
from Database.models import SalesTransaction
from sqlmodel import select


def show_product_page():

    st.title("📦 Product Analysis")

    with get_session() as session:
        data = session.exec(select(SalesTransaction)).all()

    df = pd.DataFrame([d.dict() for d in data])

    # ---------------- TOP PRODUCTS ----------------
    st.subheader("Top Products by Revenue")

    top = (
        df.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.dataframe(top)

    # ---------------- LOW MARGIN PRODUCTS ----------------
    st.subheader("Low Margin Products")

    margin = (
        df.groupby("product_name")["margin_ratio"]
        .mean()
        .sort_values()
        .reset_index()
    )

    st.dataframe(margin.head(5))

    # ---------------- SCATTER ----------------
    st.subheader("Revenue vs Margin")

    scatter = df.groupby("product_name").agg({
        "revenue": "sum",
        "margin_ratio": "mean"
    }).reset_index()

    fig = px.scatter(
        scatter,
        x="revenue",
        y="margin_ratio",
        text="product_name"
    )

    st.plotly_chart(fig, use_container_width=True)