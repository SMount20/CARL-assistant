import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

st.set_page_config(page_title="C.A.R.L. - Napleton Kia", layout="wide")
st.image("napleton_logo.jpg", width=200)
st.title("C.A.R.L. - Customer Assistant for Revenue & Leads")

@st.cache_data
def scrape_inventory():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    data = []

    for url in [
        "https://www.napletonkiaoffishers.com/new-inventory/index.htm",
        "https://www.napletonkiaoffishers.com/used-inventory/index.htm"
    ]:
        driver.get(url)
        time.sleep(5)

        cars = driver.find_elements(By.CSS_SELECTOR, ".vehicle-card, .vehicleListing")

        for car in cars:
            try:
                title = car.find_element(By.CSS_SELECTOR, ".title, .vehicle-header").text
                price = car.find_element(By.CSS_SELECTOR, ".primary-price").text
                stock = car.find_element(By.CSS_SELECTOR, ".stock-number").text.replace("Stock:", "").strip()
                img = car.find_element(By.TAG_NAME, "img").get_attribute("src")
                data.append({
                    "Title": title,
                    "Price": price,
                    "Stock #": stock,
                    "Image": img
                })
            except:
                continue

    driver.quit()
    return pd.DataFrame(data)

df = scrape_inventory()

search_query = st.text_input("Search Inventory", "")

if search_query:
    df = df[df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

st.dataframe(df)