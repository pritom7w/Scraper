from datetime import date
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://www.amazon.com/"
OUTPUT_FILE = Path("paypal_data.json")


def scrape_email(url: str) -> list[str]:
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        link[7:]
        for link in soup.find_all("a", href=True)
        if link[7:].lower().startswith("mailto:")
    ]


def main() -> None:
    emails = scrape_email(DEFAULT_URL)
    rows = [
        {"URL": DEFAULT_URL, "Email": email, "Date": date.today().isoformat()}
        for email in emails
    ]
    pd.DataFrame(rows, columns=["URL", "Email", "Date"]).to_json(
        OUTPUT_FILE,
        orient="records",
        indent=2,
    )
    print(f"Saved {len(rows)} email records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
