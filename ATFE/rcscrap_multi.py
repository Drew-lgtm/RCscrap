import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Function to scrape data from a URL and return a DataFrame
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="html.parser")
        data = str(soup.find_all("script"))
        item_names = re.findall(r"'item_name': '(.*?)'", data)
        prices = re.findall(r"'price': '(.*?)'", data)
        new_prices = [round(float(price) * 1.21) for price in prices]
        df = pd.DataFrame({"Položka": item_names, "Cena v Kč": new_prices})
        return df

# List of URLs to scrape
urls = [
    "https://www.rcobchod.cz/6207-rc-drony/strana-1-1/",
    "https://www.rcobchod.cz/6137-rc-auta/strana-1-1/",
    "https://www.rcobchod.cz/6133-rc-vrtulniky/strana-1-1/",
    "https://www.rcobchod.cz/6129-rc-tanky/strana-1-1/",
    "https://www.rcobchod.cz/6145-rc-letadla/strana-1-1/",
    "https://www.rcobchod.cz/6130-rc-lode/strana-1-1/",
    "https://www.rcobchod.cz/6138-roboti/strana-1-1/"
]

# List of sheet names in the desired order
sheet_names = ["Drony", "Auta", "Vrtulníky", "Tanky", "Letadla", "Lodě", "Roboti"]

# Create an Excel writer
excel_writer = pd.ExcelWriter("rcobchod_data_multi.xlsx", engine="xlsxwriter")

# Loop through the URLs, scrape data, and save to separate sheets in the Excel file
for i, url in enumerate(urls):
    df = scrape_data(url)
    sheet_name = sheet_names[i]
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

# Save the Excel file
excel_writer._save()

print("Data has been exported to rcobchod_data_multi.xlsx")
