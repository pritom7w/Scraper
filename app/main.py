from datetime import date
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

DEFAULT_URL = "https://www.amazon.com/"
OUTPUT_FILE = Path("paypal_data.json")


def get_url_list() -> list[str]:
    value = st.text_area("URL list", DEFAULT_URL, height=100)
    urls = [line.strip() for line in value.splitlines() if line.strip()]
    return urls or [DEFAULT_URL]


def scrape_email(url: str) -> list[str]:
    response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        href[7:]
        for link in soup.find_all("a", href=True)
        for href in [link["href"]]
        if href.lower().startswith("mailto:")
    ]


def load_scraped_data() -> pd.DataFrame:
    columns = ["URL", "Email", "Date"]
    if not OUTPUT_FILE.exists():
        return pd.DataFrame(columns=columns)
    try:
        return pd.read_json(OUTPUT_FILE).reindex(columns=columns)
    except (ValueError, OSError):
        return pd.DataFrame(columns=columns)


def save_scraped_data(rows: list[dict[str, str]]) -> pd.DataFrame:
    data = pd.DataFrame(rows, columns=["URL", "Email", "Date"])
    data.to_json(OUTPUT_FILE, orient="records", indent=2)
    return data


def main() -> None:
    st.title("Scraper")
    st.header("Command Center")
    st.sidebar.title("URL Input")

    urls = get_url_list()
    if st.button("Start scraper"):
        rows = []
        for url in urls:
            try:
                rows.extend(
                    {"URL": url, "Email": email, "Date": date.today().isoformat()}
                    for email in scrape_email(url)
                )
            except requests.RequestException as error:
                st.warning(f"Could not scrape {url}: {error}")
        data = save_scraped_data(rows)
        st.success(f"Saved {len(data)} email records.")
    else:
        data = load_scraped_data()

    st.write("Scraped Data:")
    st.dataframe(data)
    st.write("Live Log:")
    st.text(f"Loaded {len(data)} record(s).")


if __name__ == "__main__":
    main()
