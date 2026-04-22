import streamlit as st
import pandas as pd
import plotly.express as px

from Database.db import get_session
from Database.models import SalesTransaction
from sqlmodel import select


def show_comparison_page():

    st.title("📈 Comparisons")

    with get_session() as session:
        data = session.exec(select(SalesTransaction)).all()

    df = pd.DataFrame([d.dict() for d in data])

    # ---------------- QUARTERLY ----------------
    st.subheader("Revenue by Quarter")

    quarterly = (
        df.groupby("quarter")["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(quarterly, x="quarter", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- CATEGORY ----------------
    st.subheader("Revenue by Category")

    category = (
        df.groupby("category")["revenue"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(category, x="category", y="revenue")
    st.plotly_chart(fig2, use_container_width=True)