import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from components.sidebar import show_sidebar

# API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://be-budget-tracker.onrender.com"

def get_stats(date_from: datetime | None = None, date_to: datetime | None = None):
    params = ""
    if date_from:
        date_from_string = date_from.strftime("%Y-%m-%d")
        params += f'{f"&date_from={date_from_string}" if params != "" else f"date_from={date_from_string}"}'
    if date_to:
        date_to_string = date_to.strftime("%Y-%m-%d")
        params += f'{f"&date_to={date_to_string}" if params != "" else f"date_to={date_to_string}"}'
    if params != "":
        params = "?" + params
    response = requests.get(f'{API_BASE}/stats/{params}')
    if response.status_code == 200:
        data = response.json()
        return data
    return []

st.set_page_config(page_title="Dashboard", layout="centered")

show_sidebar()

st.title("Dashboard")
today = datetime.now()
first_of_month = datetime(today.year, today.month, 1)
first_of_next_month = datetime(today.year, today.month + 1, 1)
date_from = st.date_input("Date From", value=first_of_month)
date_to = st.date_input("Date To", value=first_of_next_month)
stats = get_stats(date_from=date_from, date_to=date_to)
category_names = []
for monthly_total in stats["monthly_totals"]:
    if monthly_total["category"] not in category_names:
        category_names.append(monthly_total["category"])
if len(category_names) > 0:
    columns = st.columns(len(category_names))
    for i in range(len(category_names)):
        calculated_total = 0
        for monthly_total in stats["monthly_totals"]:
            if monthly_total["category"] == category_names[i]:
                calculated_total += monthly_total["total_amount"]
        columns[i].metric(category_names[i], f'{calculated_total} RON')
    st.subheader("By Category")
    by_category_df = pd.DataFrame(stats["by_category"])
    by_category_df = by_category_df.rename(columns={"category": "Category", "total_amount": "Amount"})
    by_category_df = by_category_df.set_index("Category")
    st.bar_chart(by_category_df)
    st.subheader("Monthly Totals")
    monthly_totals_df = pd.DataFrame(stats["monthly_totals"]).rename(columns={"category": "Category", "total_amount": "Amount", "month": "Month"}).pivot(index="Month", columns="Category", values="Amount").sort_index()
    st.line_chart(monthly_totals_df)
else:
    st.warning("There is no transactions recorded, start recording to see insights!")