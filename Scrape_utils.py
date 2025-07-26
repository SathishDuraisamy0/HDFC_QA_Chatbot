import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = [
    "https://www.hdfcbank.com/personal/pay/cards/credit-cards",
    "https://www.hdfcbank.com/personal/pay/cards/debit-cards",
    "https://www.hdfcbank.com/personal/pay/cards/forex-cards",
    "https://www.hdfcbank.com/personal/pay/cards/millennia-cards",
]

cards_info = {}

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for card in soup.find_all("div", class_="cardWrapper"):
            title_tag = card.find("span", class_="card-name")
            desc_tag = card.find("div", class_="card-des")

            if title_tag and desc_tag:
                title = title_tag.get_text(strip=True)
                desc = desc_tag.get_text(strip=True)
                cards_info[title] = desc

    except Exception as e:
        print(f"Error while processing {url}: {e}")

# Convert to DataFrame
df = pd.DataFrame(cards_info.items(), columns=["Products", "Description"])
