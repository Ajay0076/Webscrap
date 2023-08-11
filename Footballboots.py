import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = ("https://www.amazon.in/s?k=football+boots&sprefix=football+boo%2Caps%2C232&ref=nb_sb_ss_ts-doa-p_1_12")

headers = {
    "User-Agent": "Your User Agent String"
}

max_retries = 5
retry_delay = 5  # seconds

boots_data = []

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
boot_cards = soup.find_all("div", class_="s-result-item")

for boot_card in boot_cards:
    try:
        boot_name_elem = boot_card.find("span", class_="a-size-base-plus a-color-base a-text-normal")
        boot_name = boot_name_elem.text.strip() if boot_name_elem else "N/A"

        boot_price_elem = boot_card.find("span", class_="a-offscreen")
        boot_price = boot_price_elem.text.strip() if boot_price_elem else "N/A"

        boot_rating_elem = boot_card.find("span", class_="a-icon-alt")
        boot_rating = boot_rating_elem.text.strip() if boot_rating_elem else "N/A"

        boots_data.append({
            "Name": boot_name,
            "Price": boot_price,
            "Rating": boot_rating
        })
    except Exception as e:
        print("Error in extracting boot data:", e)

df = pd.DataFrame(boots_data)
df.to_csv("amazon_football_boots.csv", index=False)

print("Data successfully extracted and CSV saved.")
