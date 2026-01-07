import streamlit as st
import requests
from datetime import datetime
from components.sidebar import show_sidebar

API_BASE = "http://127.0.0.1:8000"

def show_table_header():
    columns = st.columns((1, 2, 1, 2, 2, 1, 1))
    columns_names = ["Id", "Description", "Amount", "Created At", "Category Id", "Edit", "Delete"]
    for column, field_name in zip(columns, columns_names):
        column.write(field_name)

def show_table_body(target_category_id: int | None = None, date_from: datetime | None = None, date_to: datetime | None = None):
    transactions = get_transactions(target_category_id=target_category_id, date_from=date_from, date_to=date_to)
    for transaction in transactions:
        show_table_row(transaction=transaction)

def show_table_row(transaction):
    col1, col2, col3, col4, col5, col6, col7 = st.columns((1, 2, 1, 2, 2, 1, 1))
    col1.write(transaction["id"])
    col2.write(transaction["description"])
    col3.write(transaction["amount"])
    col4.write(transaction["created_at"])
    col5.write(transaction["category_id"])
    col6_sh = col6.empty()
    do_edit_action = col6_sh.button("Edit", key=f'edit_{transaction["id"]}')
    if do_edit_action:
        handle_edit(transaction_id=transaction["id"])
    col7_sh = col7.empty()
    do_delete_action = col7_sh.button("🗑", key=f'delete={transaction["id"]}')
    if do_delete_action:
        handle_delete(transaction_id=transaction["id"])

def get_transactions(target_category_id: int | None = None, date_from: datetime | None = None, date_to: datetime | None = None):
    params = ""
    if target_category_id:
        params += f'{f"&category_id={target_category_id}" if params != "" else f"category_id={target_category_id}"}'
    if date_from:
        date_from_string = date_from.strftime("%Y-%m-%d")
        params += f'{f"&date_from={date_from_string}" if params != "" else f"date_from={date_from_string}"}'
    if date_to:
        date_to_string = date_to.strftime("%Y-%m-%d")
        params += f'{f"&date_to={date_to_string}" if params != "" else f"date_to={date_to_string}"}'
    if params != "":
        params = "?" + params
    response = requests.get(f'{API_BASE}/transactions/{params}')
    if response.status_code == 200:
        data = response.json()
        return data
    return []

def get_transaction(transaction_id: int):
    response = requests.get(f'{API_BASE}/transactions/{transaction_id}')
    if response.status_code == 200:
        data = response.json()
        return data
    return {}

def get_child_categories():
    response = requests.get(f'{API_BASE}/categories/')
    if response.status_code == 200:
        data = response.json()
        children = []
        for cat in data:
            if cat["is_parent"]:
                children.extend(cat["children"])
        return children
    return []

def get_suggested_category(keyword: str) -> int | None:
    response = requests.post(f'{API_BASE}/categorize/', json={"description": keyword})
    if response.status_code == 200:
        data = response.json()
        st.toast(f'Suggested category is: {data["category_name"]}, because: {data["reason"]}')
        return data["category_id"]
    st.toast(f'Could not categorize keyword: {keyword}')
    return None

def handle_delete(transaction_id: int):
    response = requests.delete(f'{API_BASE}/transactions/{transaction_id}')
    if response.status_code == 204:
        st.rerun()

def handle_edit(transaction_id: int):
    create_edit_modal(transaction_id=transaction_id)

@st.dialog("Edit Transaction")
def create_edit_modal(transaction_id: int):
    transaction = get_transaction(transaction_id=transaction_id)
    transaction_desc = st.text_input("Description", value=transaction["description"])
    suggested_category_id = None
    if st.button("Suggest Category", type="secondary"):
        suggested_category_id = get_suggested_category(transaction_desc)
    transaction_amount = st.number_input("Amount", value=transaction["amount"])
    transaction_date = st.datetime_input("Created At", value=transaction["created_at"])
    child_categories = get_child_categories()
    category_names = []
    category_ids = {}
    for category in child_categories:
        category_names.append(category["name"])
        category_ids[category["name"]] = category["id"]
    target_category_name = ""
    for key, value in category_ids.items():
        if (not suggested_category_id and value == transaction["category_id"]) or value == suggested_category_id:
            target_category_name = key
    target_index = 0
    for i in range(len(category_names)):
        if category_names[i] == target_category_name:
            target_index = i
    transaction_cat = st.selectbox("Category", category_names, index=target_index)
    if st.button("Save"):
        if transaction_desc and transaction_amount and transaction_date and transaction_cat:
            formatted_datetime = transaction_date.strftime("%Y-%m-%dT%H:%M:%S")
            response = requests.put(f'{API_BASE}/transactions/{transaction["id"]}', json={"description": transaction_desc, "amount": transaction_amount, "created_at": formatted_datetime, "category_id": category_ids[transaction_cat] if transaction_cat is not None else None})
            if response.status_code == 200:
                st.rerun()
        else:
            st.toast("Please fill in the required information!")

@st.dialog("Add new Transaction")
def create_add_modal():
    transaction_desc = st.text_input("Description", placeholder="Add the description")
    suggested_category_id = None
    if st.button("Suggest Category", type="secondary"):
        suggested_category_id = get_suggested_category(transaction_desc)
    transaction_amount = st.number_input("Amount", placeholder=100.00, step=1.00)
    transaction_date = st.datetime_input("Created At", value=None)
    child_categories = get_child_categories()
    category_names = []
    category_ids = {}
    for category in child_categories:
        category_names.append(category["name"])
        category_ids[category["name"]] = category["id"]
    target_index = None
    if suggested_category_id:
        for key, value in category_ids.items():
            if value == suggested_category_id:
                target_category_name = key
        for i in range(len(category_names)):
            if category_names[i] == target_category_name:
                target_index = i
    transaction_cat = st.selectbox("Category", category_names, index=target_index, placeholder="Select the category")
    if st.button("Save"):
        if transaction_desc and transaction_amount and transaction_date:
            formatted_datetime = transaction_date.strftime("%Y-%m-%dT%H:%M:%S")
            response = requests.post(f'{API_BASE}/transactions/', json={"description": transaction_desc, "amount": transaction_amount, "created_at": formatted_datetime, "category_id": category_ids[transaction_cat] if transaction_cat is not None else None})
            if response.status_code == 201:
                st.rerun()
        else:
            st.toast("Please fill in the required information!")

st.set_page_config(page_title="Transactions", layout="centered")

show_sidebar()

st.title("Transactions")
categories = get_child_categories()
category_names = ["All"]
category_ids = {}
for category in categories:
    category_names.append(category["name"])
    category_ids[category["name"]] = category["id"]
target_category_name = st.selectbox("Category", category_names, index=0)
target_category_index = None if target_category_name == "All" else category_ids[target_category_name]
date_from = st.date_input("Date From", value=None)
date_to = st.date_input("Date To", value=None)
st.subheader("List of Transactions")
show_table_header()
show_table_body(target_category_id=target_category_index, date_from=date_from, date_to=date_to)
st.subheader("Actions")
if st.button("Add new"):
    create_add_modal()