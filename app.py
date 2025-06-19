import streamlit as st
import pandas as pd

st.set_page_config(page_title="C.A.R.L. - Napleton Kia", layout="wide")

st.image("napleton_logo.jpg", width=200)
st.title("C.A.R.L. - Customer Assistant for Revenue & Leads")

search_query = st.text_input("Search Inventory", "")

# Placeholder: load data
@st.cache_data
def load_data():
    return pd.DataFrame([
        {"Stock": "FWHO12345", "Model": "Telluride", "Price": 44995, "Used/New": "New"},
        {"Stock": "FRSL54321", "Model": "Sportage", "Price": 28995, "Used/New": "Used"},
    ])

df = load_data()

# Simple search
if search_query:
    df = df[df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

st.dataframe(df)