import pandas as pd
import requests
from openpyxl import load_workbook

# Your API Key and Search Engine ID
API_KEY = "AIzaSyDiAPsN1oxtg2f-Qj_p4xUr-iaYbm7eMn4"
SEARCH_ENGINE_ID = "7626935c7bf8f43fa"

# Read the contacts from Excel
input_file = "data.xlsx"
output_file = "car_dealership_results.xlsx"
contacts_df = pd.read_excel(input_file)

# Keywords to filter car-related results
car_keywords = ["car", "auto", "vehicle", "dealership", "automobile", "motor"]

# Function to search for a phone number
def search_phone_number(phone_number):
    query = phone_number
    url = f"https://www.googleapis.com/customsearch/v1?q=+{query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if "items" in data:
            return data["items"][0]  # Only return the top result
    else:
        print(f"Request failed, response code:{response.status_code}")
    return None

# Function to check if a result is car-related
def is_car_related(result):
    content = f"{result.get('title', '')} {result.get('snippet', '')} {result.get('link', '')}".lower()
    return any(keyword in content for keyword in car_keywords)

i=0
# Iterate through contacts and search
for index, row in contacts_df.iterrows():
    i+=1
    if(i==2):
        break
    phone_number = row["Number"]
    search_result = search_phone_number(phone_number)
    print(search_result)
    if search_result:
        if is_car_related(search_result):
            result = {
                "Phone Number": phone_number,
                "Title": search_result["title"],
                "Link": search_result["link"],
                "Snippet": search_result["snippet"],
            }
            print(f"Match found: {result}")
            
            # Append the result to the output file
            try:
                # Check if the output file exists
                with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                    pd.DataFrame([result]).to_excel(writer, index=False, header=not writer.book.sheetnames)
            except FileNotFoundError:
                # Create a new file if it doesn't exist
                pd.DataFrame([result]).to_excel(output_file, index=False)
        else:
            print(f"No car-related keywords in the top result for {phone_number}.")
    else:
        print(f"No results found for {phone_number}.")
    
    # Optional: Print progress every 100 contacts
    if (index + 1) % 100 == 0:
        print(f"Processed {index + 1} contacts...")

print("Processing complete.")
