from typing import Iterable
import streamlit as st
import requests
import pandas as pd
from components.sidebar import show_sidebar

# API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://be-budget-tracker.onrender.com"

categories = {"All": None}

st.set_page_config(page_title="Category Keywords", layout="centered")

show_sidebar()

def get_categories() -> Iterable[str]:
    response = requests.get(f'{API_BASE}/categories/')
    if response.status_code == 200:
        data = response.json()
        category_names = []
        for row in data:
            if row["is_parent"]:
                for child in row["children"]:
                    categories[child["name"]] = child["id"]
                    category_names.append(child["name"])
            else:
                categories[row["name"]] = row["id"]
                category_names.append(row["name"])
        return category_names
    return []

def get_keywords(category_id: int | None = None) -> pd.DataFrame:
    response = requests.get(f'{API_BASE}/keywords{("" if category_id is None else f"?category_id={category_id}")}')
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=["id", "keyword", "category_id"])
        return df
    return pd.DataFrame()

def render_dataframe(df: pd.DataFrame):
    st.dataframe(
        df, 
        column_order=["id", "keyword", "category_id"], 
        column_config={
            "id": st.column_config.NumberColumn(label="Id"),
            "keyword": st.column_config.TextColumn(label="Keyword"),
            "category_id": st.column_config.NumberColumn(label="Category Id"),
        },
        hide_index=True
    )

@st.dialog("Add new Category Keyword")
def create_add_modal():
    keyword = st.text_input("Keyword", placeholder="Input your keyword")
    option = st.selectbox("Select category", get_categories(), placeholder="Select category", index=None)
    if st.button("Add"):
        if keyword and option:
            response = requests.post(f'{API_BASE}/keywords/', json={"keyword": keyword, "category_id": categories[option]})
            if response.status_code == 201:
                st.rerun()
        else:
            st.toast("Please fill in the required information!")

@st.dialog("Delete Category Keyword")
def create_delete_modal():
    keywords = get_keywords()
    keywords_cleaned = keywords["keyword"]
    option = st.selectbox("Select keyword", keywords_cleaned, placeholder="Select keyword", index=None)
    if st.button("Delete"):
        if option:
            target_keyword_id = keywords[keywords["keyword"] == option]["id"].to_list()[0]
            response = requests.delete(f'{API_BASE}/keywords/{target_keyword_id}')
            if response.status_code == 204:
                st.rerun()
        else:
            st.toast("Please select a keyword to delete!")

st.title("Category Keywords")
temp_cat = ["All"]
for cat in get_categories():
    temp_cat.append(cat)
option = st.selectbox("Select category", temp_cat, placeholder="Select category")
st.subheader("List of Keywords")
if option:
    render_dataframe(get_keywords(categories[option]))
else:
    render_dataframe(get_keywords())
st.subheader("Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("Add new"):
        create_add_modal()
with col2:
    if st.button("Delete"):
        create_delete_modal()

# st.header("Autocategorize test")
# description = st.text_input("Transaction description")
# if st.button("Suggest category"):
#     if description:
#         response = requests.post(f'{API_BASE}/categorize/', json={"description": description})
#         if response.status_code == 200:
#             data = response.json()
#             if data["category_name"]:
#                 st.success(f'Suggested category: {data["category_name"]}\nReason: {data["reason"]}')
#             else:
#                 st.warning("No category suggestion")
#         else:
#             st.error("Backend error")