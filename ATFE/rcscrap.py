import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# URL of the page you want to scrape
url = "https://www.rcobchod.cz/6442-drony-s-fpv-prenosem/strana-1-1/"

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

    # Create a DataFrame from the item names and prices
    df = pd.DataFrame({"Item Name": item_names, "Price": new_prices})

    # Remove duplicates based on "Item Name" and "Price" columns
    df.drop_duplicates(subset=["Item Name", "Price"], inplace=True)

    # Export the DataFrame to an Excel file named "rcobchod_data.xlsx"
    df.to_excel("rcobchod_data.xlsx", index=False)

    print("Data has been exported to rcobchod_data.xlsx")
