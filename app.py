import streamlit as st
import pandas as pd
from requests_html import HTMLSession

st.set_page_config(page_title="C.A.R.L. - Napleton Kia", layout="wide")
st.image("napleton_logo.jpg", width=200)
st.title("C.A.R.L. - Customer Assistant for Revenue & Leads")

@st.cache_data
def scrape_inventory():
    session = HTMLSession()
    inventory = []

    urls = [
        "https://www.napletonkiaoffishers.com/new-inventory/index.htm",
        "https://www.napletonkiaoffishers.com/used-inventory/index.htm"
    ]

    for url in urls:
        r = session.get(url)
        r.html.render(timeout=20)
        listings = r.html.find(".vehicle-card, .vehicleListing")

        for listing in listings:
            try:
                title = listing.find(".title, .vehicle-header", first=True).text
                price = listing.find(".primary-price", first=True).text
                stock_el = listing.find(".stock-number", first=True)
                stock = stock_el.text.replace("Stock:", "").strip() if stock_el else ""
                image = listing.find("img", first=True).attrs.get("src", "")

                inventory.append({
                    "Title": title,
                    "Price": price,
                    "Stock #": stock,
                    "Image": image
                })
            except:
                continue

    return pd.DataFrame(inventory)

df = scrape_inventory()

# UI filters
st.sidebar.header("Search Filters")
search_text = st.sidebar.text_input("Search Term (Model/Keyword)")
stock_search = st.sidebar.text_input("Stock #")
min_price = st.sidebar.number_input("Min Price", min_value=0, value=0)
max_price = st.sidebar.number_input("Max Price", min_value=0, value=100000)
is_suv = st.sidebar.checkbox("Only show SUVs")
is_awd = st.sidebar.checkbox("Only show AWD")

# Apply filters
if search_text:
    df = df[df.apply(lambda x: search_text.lower() in str(x).lower(), axis=1)]

if stock_search:
    df = df[df["Stock #"].str.contains(stock_search, case=False)]

df["Clean Price"] = df["Price"].replace('[\$,]', '', regex=True).astype(float)
df = df[(df["Clean Price"] >= min_price) & (df["Clean Price"] <= max_price)]

if is_suv:
    df = df[df["Title"].str.contains("SUV", case=False)]

if is_awd:
    df = df[df["Title"].str.contains("AWD", case=False)]

st.dataframe(df.drop(columns=["Clean Price"]))