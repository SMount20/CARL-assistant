import streamlit as st
import pandas as pd

st.set_page_config(page_title="C.A.R.L.", layout="wide")
st.title("C.A.R.L. — Customer Assistant for Revenue & Leads")
st.markdown("Talk to C.A.R.L. below:")

prompt = st.text_area("Enter a dealership scenario:")
if st.button("Generate Response"):
    st.write("Response for:", prompt)

uploaded_file = st.file_uploader("Upload Inventory CSV", key="inventory_upload")

if uploaded_file is not None:
    try:
        # Try reading as UTF-8 with BOM (common for Excel exports)
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
    else:
        st.dataframe(df)

st.markdown("Reminders coming soon!")
