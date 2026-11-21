import json
from datetime import date

import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com/"

def main():
    response = requests.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )
    response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Replace this with the actual extraction logic you need.
    result = {
        "date": date.today().isoformat(),
        "url": URL,
        "title": soup.title.get_text(strip=True) if soup.title else None,
    }

with open("paypal_data.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
