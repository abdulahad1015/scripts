import requests
from bs4 import BeautifulSoup
import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets connection
# def connect_to_google_sheet(sheet_name):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     credentials = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
#     client = gspread.authorize(credentials)
#     return client.open(sheet_name).sheet1

# Scrape data from the website
def scrape_memory_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    products = soup.find_all("div", class_="product-single-card")  # Adjust this selector based on site structure
    for product in products:
        # Extracting the image source URL
        img_tag = product.find("img",recursive=True)       
        print(img_tag)
        
        # Extracting product details
        card_div = product.find("div", class_="p-details")
        card_text = card_div.get_text(strip=True) if card_div else "N/A"
        title = product.find("h2", class_="p-title").get_text(strip=True) if product.find("h2", class_="p-title") else "N/A"
        price = product.find("span", class_="p-price").get_text(strip=True) if product.find("span", class_="p-price") else "N/A"
        table = card_div.find("table", recursive=True) if card_div and card_div.find("table", recursive=True) else "N/A"

        # Adding the extracted data to the list
        data.append([title, price, table])
    
    return data

# Append data to Google Sheet
# def append_to_google_sheet(sheet, data):
#     for row in data:
#         sheet.append_row(row)

if __name__ == "__main__":
    url = "https://www.memoryclearance.com/categories/memory.html"

    # Scrape data
    memory_data = scrape_memory_data(url)

    # Append to Google Sheet
    # append_to_google_sheet(sheet, memory_data)
    
    # Print the scraped data
    for i in memory_data:
        print(i)

    print("Data successfully scraped and printed.")
