import streamlit as st
import requests
from components.sidebar import show_sidebar

# API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://be-budget-tracker.onrender.com"

def show_table_header():
    columns = st.columns((1, 2, 1, 1, 1, 1))
    columns_names = ["Id", "Name", "Is Parent", "Parent Id", "Edit", "Delete"]
    for column, field_name in zip(columns, columns_names):
        column.write(field_name)

def show_table_body():
    categories = get_categories()
    for category in categories:
        show_table_row(category=category)
        if category["is_parent"]:
            for child in category["children"]:
                show_table_row(child)

def show_table_row(category):
    col1, col2, col3, col4, col5, col6 = st.columns((1, 2, 1, 1, 1, 1))
    col1.write(category["id"])
    col2.write(category["name"])
    col3.write(category["is_parent"])
    col4.write(category["parent_id"])
    col5_sh = col5.empty()
    do_edit_action = col5_sh.button("Edit", key=f'edit_{category["id"]}')
    if do_edit_action:
        handle_edit(category_id=category["id"])
    col6_sh = col6.empty()
    do_delete_action = col6_sh.button("Delete", key=f'delete={category["id"]}')
    if do_delete_action:
        handle_delete(category_id=category["id"])

def handle_delete(category_id: int):
    response = requests.delete(f'{API_BASE}/categories/{category_id}')
    if response.status_code == 204:
        st.rerun()

def handle_edit(category_id: int):
    create_edit_modal(category_id=category_id)

def get_categories():
    response = requests.get(f'{API_BASE}/categories/')
    if response.status_code == 200:
        data = response.json()
        return data
    return {}

def get_category(category_id: int):
    response = requests.get(f'{API_BASE}/categories/{category_id}')
    if response.status_code == 200:
        data = response.json()
        return data
    return data

@st.dialog("Add new Category")
def create_add_modal():
    category_name = st.text_input("Category Name", placeholder="Input the category name")
    is_parent = st.checkbox("Is parent")
    categories = get_categories()
    category_names = []
    category_ids = {}
    for category in categories:
        category_names.append(category["name"])
        category_ids[category["name"]] = category["id"]
    parent_category = st.selectbox("Parent Category", category_names, placeholder="Select category", index=None, disabled=is_parent)
    if st.button("Add"):
        if category_name and ((not is_parent and parent_category) or (is_parent and not parent_category)):
            response = requests.post(f'{API_BASE}/categories/', json={"name": category_name, "is_parent": is_parent, "parent_id": category_ids[parent_category] if not is_parent else None})
            if response.status_code == 201:
                st.rerun()
        else:
            st.toast("Please fill in the required information!")

@st.dialog("Edit Category")
def create_edit_modal(category_id: int):
    category = get_category(category_id=category_id)
    category_name = st.text_input("Category Name", value=category["name"])
    if st.button("Save"):
        if category_name:
            response = requests.put(f'{API_BASE}/categories/{category["id"]}', json={"name": category_name, "is_parent": category["is_parent"], "parent_id": category["parent_id"]})
            if response.status_code == 200:
                st.rerun()
        else:
            st.toast("Please fill in the required information!")

st.set_page_config(page_title="Categories", layout="centered")

show_sidebar()

st.title("Categories")
st.subheader("List of Categories")
show_table_header()
show_table_body()
st.subheader("Actions")
if st.button("Add new"):
    create_add_modal()