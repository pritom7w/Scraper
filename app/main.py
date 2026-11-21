import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime

def get_url_list():
    if not st.text_input("Upload List: ", "https://www.amazon.com/"):
        return ["https://www.amazon.com/"]
    else:
        url_list = st.text_input("Upload List: ").splitlines() + ["https://www.amazon.com/"]
        return url_list

def scrape_email(url):
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, "lxml")
    emails = soup.find_all("a", {"href": {"startswith": "mailto:"}})
    email_list = [email.text for email in emails]
    return email_list

def load_scraped_data():
    filename = f"{dt.date.today().strftime('%Y-%m-%d')}_paypal_data.json"
    if st.checkbox("Upload List"):
        df = pd.read_csv(filename, sep="\n")
    else:
        df = pd.read_json(filename)
    df["Date"] = df["URL"].apply(lambda x: dt.datetime.fromisoformat(x).strftime("%Y-%m-%d"))
    df = df.drop("URL", axis=1)
    return df

def save_scraped_data(data, filename):
    df = pd.DataFrame(data)
    df["Date"] = df["URL"].apply(lambda x: dt.datetime.now().strftime("%Y-%m-%d"))
    df.to_csv(filename, index=False)
    
def main():
    url_list = get_url_list()
    data = []
    for url in url_list:
        emails = scrape_email(url)
        if emails:
            data.append({"URL": url, "Email": emails[0]})
    df = pd.DataFrame(data)
    df["Date"] = df["URL"].apply(lambda x: dt.datetime.now().strftime("%Y-%m-%d"))
    df = df.drop("URL", axis=1)
    load_scraped_data()
    stylize(df, warn=True)
    st.title("Scraper")
    st.header("Command Center")
    st.sidebar.title("URL Input")
    st.sidebar.write("Single Target Scraping")
    st.sidebar.write("Upload List: ")
    st.sidebar.checkbox("Upload List", value=True)
    st.sidebar.button("Refresh")
    st.sidebar.button("Start/Stop Scraper")
    st.sidebar.button("About")
    st.sidebar.button("Exit")
    st.write(stylize(df, warn=True)
    st.write("Scraped Data:")
    st.dataframe(df)
    st.write("Live Log:")
    st.text("Scraping...Found Email: user@amazon.comStatus: Active")
    st.write("Real-Time Millisecond Monitor:")
    st.write("Millisecond Monitor")
    st.write("Search:")
    st.text("")
    st.dataframe(df)
    
if __name__ == "__main__":
    main()
