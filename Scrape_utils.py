import requests
from bs4 import BeautifulSoup

def scrape_hdfc_cards():
    urls = [
        "https://www.hdfcbank.com/personal/pay/cards/credit-cards",
        "https://www.hdfcbank.com/personal/pay/cards/debit-cards",
        "https://www.hdfcbank.com/personal/pay/cards/forex-cards",
        "https://www.hdfcbank.com/personal/pay/cards/millennia-cards",
    ]

    data = []
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for card in soup.find_all("div", class_="cardWrapper"):
                name = card.find("span", class_="card-name")
                desc = card.find("div", class_="card-des")
                if name and desc:
                    data.append({
                        "Products": name.get_text(strip=True),
                        "Description": desc.get_text(strip=True)
                    })
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return data