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
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(uploaded_file, encoding='cp1252')
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
            else:
                st.success("Read with cp1252 encoding")
        else:
            st.success("Read with ISO-8859-1 encoding")
    else:
        st.success("Read with UTF-8-SIG encoding")

    try:
        st.dataframe(df)
    except:
        st.warning("Data loaded, but table failed to render.")

st.markdown("Reminders coming soon!")
