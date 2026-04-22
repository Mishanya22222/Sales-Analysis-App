import streamlit as st
import pandas as pd
from ETL.validate import validate_columns
from ETL.transform import transform_data
from Database.db import create_db_and_tables, get_session
from Database.crud import insert_dataframe
import streamlit as st
from ui.dashboard import show_dashboard
from ui.product_page import show_product_page
from ui.comparison_page import show_comparison_page


create_db_and_tables()

st.title("Sales Intelligence Copilot")
st.write("Let's analyze your sales data and uncover insights together!")

st.write("Please upload your sales data in CSV format. The dataset should include the following columns: `order_date`, `product_name`, `category`, `quantity`, `unit_price`, and `unit_variable_cost`.")
uploaded_file = st.file_uploader("Upload your sales data (CSV format)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("Raw Data Preview:")
    st.dataframe(df.head())

    valid, message = validate_columns(df)
    if not valid:
        st.error(message)
    else:
        st.success(message)

        df = transform_data(df)

        st.write("Processed Data Preview")
        st.dataframe(df.head())

        with get_session() as session:
            inserted_count, skipped_count = insert_dataframe(session, df)
            if inserted_count == 0:
                st.info("Dataset already exists in database. No new rows inserted.")
            else:
                st.success(
                    f"Inserted {inserted_count} new rows. "
                    f"Skipped {skipped_count} duplicate rows."
                )
    # Select page            
    st.sidebar.title("Navigation")

    page = st.sidebar.radio("Go to", [
        "Dashboard",
        "Product Analysis",
        "Comparisons"
    ])

    if page == "Dashboard":
        show_dashboard()

    elif page == "Product Analysis":
        show_product_page()

    elif page == "Comparisons":
        show_comparison_page()
