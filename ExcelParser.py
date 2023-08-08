import openpyxl
from openpyxl.styles import PatternFill
from bs4 import BeautifulSoup
import requests
import re
import time

# Load the Excel file
file_path = "INPUT.xlsx"
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# Define a fill style for the "ok" cell
fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")

# Start the timer
start_time = time.time()

# Calculate the total number of rows to process
total_rows = sheet.max_row - 1  # Subtract 1 for the header row

# Iterate through the rows in the sheet
for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=5, max_col=5):
    cell = row[0]  # Get the cell in column E for each row
    if isinstance(cell.value, str) and cell.value.lower().startswith("https"):
        sheet.cell(row=cell.row, column=8, value="ok")  # Write "ok" in column H
        sheet.cell(row=cell.row, column=8).fill = fill  # Apply the fill style

        # Get the URL from the cell
        url = cell.value

        # Scrape the title of the web page using Beautiful Soup
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text()

                # Keep only the last two words from the title
                title_words = title.split()
                if title_words:
                    work_string = ' '.join(title_words[-5:-2])
                    new_title = ""
                    for i in work_string:
                      if i.isdigit():
                        new_title = new_title + i
                else:
                    new_title = title

                sheet.cell(row=cell.row, column=9, value=title)  # Write title in column I
                sheet.cell(row=cell.row, column=10, value=new_title)  # Write new title in column J


# Save the modified Excel file
output_path = "EDITED_INPUT.xlsx"
wb.save(output_path)

# Calculate and print the duration
end_time = time.time()
duration = end_time - start_time
print("\nScript duration:", duration, "seconds")
print("Done. Check the modified Excel file")
