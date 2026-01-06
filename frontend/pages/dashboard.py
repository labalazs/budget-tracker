import streamlit as st
from components.sidebar import show_sidebar

show_sidebar()

st.title("Dashboard")
st.write("Monthly statistics and charts")
st.metric("Total Expenses", "57 RON")
st.metric("Total Income", "20 RON")