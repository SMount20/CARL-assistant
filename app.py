import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="C.A.R.L. - Napleton Kia", layout="wide")

st.image("napleton_logo.jpg", width=200)
st.title("C.A.R.L. - Customer Assistant for Revenue & Leads")

@st.cache_data
def scrape_inventory():
    base_urls = [
        "https://www.napletonkiaoffishers.com/new-inventory/index.htm",
        "https://www.napletonkiaoffishers.com/used-inventory/index.htm"
    ]
    all_data = []
    for url in base_urls:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        vehicles = soup.select(".vehicle-card")
        for v in vehicles:
            title = v.select_one(".title") or v.select_one(".vehicle-header")
            price = v.select_one(".primary-price")
            stock = v.select_one(".stock-number")
            img = v.select_one("img")
            all_data.append({
                "Title": title.text.strip() if title else "N/A",
                "Price": price.text.strip() if price else "N/A",
                "Stock #": stock.text.strip().replace("Stock:", "").strip() if stock else "N/A",
                "Image": img['src'] if img and img.get("src") else ""
            })
    return pd.DataFrame(all_data)

df = scrape_inventory()

search_query = st.text_input("Search Inventory", "")

if search_query:
    df = df[df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

st.dataframe(df)