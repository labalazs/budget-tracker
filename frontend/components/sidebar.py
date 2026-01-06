import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.title("Budget Tracker")
        st.caption("Personal finance made easy")
        
        st.markdown("---")
        st.page_link(st.Page("./streamlit_app.py"), label="Home")
        st.page_link(st.Page("./pages/dashboard.py"), label="Dashboard")
        st.page_link(st.Page("./pages/transactions.py"), label="Transactions")
        st.page_link(st.Page("./pages/categories.py"), label="Categories")
        st.page_link(st.Page("./pages/keywords.py"), label="Category Keywords")
        st.markdown("---")
        st.caption("EKKE MPPNy v1.0")
