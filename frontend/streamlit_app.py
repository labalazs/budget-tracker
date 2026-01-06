import streamlit as st
from components.sidebar import show_sidebar

st.set_page_config(page_title="Budget Tracker", layout="centered")

show_sidebar()

st.title("Welcome!")
st.write("Live consciously, spend consciously!")
st.space("large")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Dashboard")
    st.page_link(st.Page("./pages/dashboard.py"), label="See how you spend your money!")
    st.space("large")
    st.subheader("Categories")
    st.page_link(st.Page("./pages/categories.py"), label="Edit your categories!")
with col2:
    st.subheader("Transactions")
    st.page_link(st.Page("./pages/transactions.py"), label="Record a transaction!")
    st.space("large")
    st.subheader("Category Keywords")
    st.page_link(st.Page("./pages/keywords.py"), label="Edit category keywords!")