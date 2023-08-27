import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# List of URLs to scrape
urls = [
    "https://www.rcobchod.cz/6207-rc-drony/strana-1-1/",
    "https://www.rcobchod.cz/6137-rc-auta/strana-1-1/",
    "https://www.rcobchod.cz/6133-rc-vrtulniky/strana-1-1/",
    "https://www.rcobchod.cz/6129-rc-tanky/strana-1-1/",
    "https://www.rcobchod.cz/6145-rc-letadla/strana-1-1/",
    "https://www.rcobchod.cz/6130-rc-lode/strana-1-1/",
    "https://www.rcobchod.cz/6138-roboti/strana-1-1/",
]

# Initialize lists to store data from all URLs
all_item_names = []
all_prices = []

for url in urls:
    # Send an HTTP GET request to fetch the web page
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup and lxml parser
        soup = BeautifulSoup(response.content, features="html.parser")

        # Find all script tags containing product data
        data = str(soup.find_all("script"))

        # Use regular expression to find all item names and prices
        item_names = re.findall(r"'item_name': '(.*?)'", data)
        prices = re.findall(r"'price': '(.*?)'", data)
        new_prices = [round(float(price) * 1.21) for price in prices]

        # Extend the lists with data from the current URL
        all_item_names.extend(item_names)
        all_prices.extend(new_prices)

# Create a DataFrame from all the item names and prices
df = pd.DataFrame({"Item Name": all_item_names, "Price": all_prices})

# Remove duplicates based on "Item Name" column
df.drop_duplicates(subset=["Item Name"], inplace=True)

# Export the DataFrame to an Excel file named "ALL_rcobchod_data.xlsx"
df.to_excel("ALL_rcobchod_data.xlsx", index=False)

print("Data has been exported to ALL_rcobchod_data.xlsx")
