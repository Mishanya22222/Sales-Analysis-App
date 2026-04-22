import streamlit as st
import pandas as pd
import plotly.express as px

from sqlmodel import select, func
from Database.db import get_session
from Database.models import SalesTransaction


def show_dashboard():

    st.title("📊 Sales Dashboard")

    # ---------------- FILTERS ----------------
    with get_session() as session:
        categories = session.exec(
            select(SalesTransaction.category).distinct()
        ).all()

        regions = session.exec(
            select(SalesTransaction.region).distinct()
        ).all()

    selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
    selected_region = st.sidebar.selectbox("Region", ["All"] + regions)

    # ---------------- BASE QUERY ----------------
    with get_session() as session:
        query = select(SalesTransaction)

        if selected_category != "All":
            query = query.where(SalesTransaction.category == selected_category)

        if selected_region != "All":
            query = query.where(SalesTransaction.region == selected_region)

        data = session.exec(query).all()

    df = pd.DataFrame([d.dict() for d in data])

    if df.empty:
        st.warning("No data for selected filters")
        return

    # ---------------- KPI CARDS ----------------
    total_revenue = df["revenue"].sum()
    total_margin = df["contribution_margin"].sum()
    margin_ratio = total_margin / total_revenue if total_revenue else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Revenue", f"${total_revenue:,.0f}")
    col2.metric("Margin", f"${total_margin:,.0f}")
    col3.metric("Margin %", f"{margin_ratio:.2%}")

    st.divider()

    # ---------------- REVENUE TREND ----------------
    st.subheader("Revenue Over Time")

    df["order_date"] = pd.to_datetime(df["order_date"])
    trend = df.groupby("order_date")["revenue"].sum().reset_index()

    fig = px.line(trend, x="order_date", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- TOP PRODUCTS ----------------
    st.subheader("Top Products")

    top_products = (
        df.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    fig2 = px.bar(top_products, x="product_name", y="revenue")
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- INSIGHT ----------------
    top_product = top_products.iloc[0]["product_name"]

    st.info(f"Top performing product: {top_product}")