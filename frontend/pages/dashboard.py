import streamlit as st
from components.sidebar import show_sidebar

st.set_page_config(page_title="Dashboard", layout="centered")

show_sidebar()

st.title("Dashboard")
st.write("Monthly statistics and charts")
st.metric("Total Expenses", "57 RON")
st.metric("Total Income", "20 RON")