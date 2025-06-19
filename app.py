import streamlit as st
import pandas as pd

st.set_page_config(page_title="C.A.R.L.", layout="wide")
st.title("C.A.R.L. — Customer Assistant for Revenue & Leads")
st.markdown("Talk to C.A.R.L. below:")

prompt = st.text_area("Enter a dealership scenario:")
if st.button("Generate Response"):
    st.write("Response for:", prompt)

uploaded_file = st.file_uploader("Upload Inventory CSV")
uploaded_file = st.file_uploader("Upload Inventory CSV")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    
    st.dataframe(df)

st.markdown("Reminders coming soon!")
