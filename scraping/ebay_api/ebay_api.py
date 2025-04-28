import requests

# eBay API Endpoint
url = "https://api.ebay.com/sell/inventory/v1/inventory_item/abd00001"

# OAuth Token (Replace with your valid access token)
ACCESS_TOKEN = "v^1.1#i^1#f^0#r^0#p^3#I^3#t^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"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept":"application/json",
    "Content-Type": "application/json",
    "Content-Language": "en-US"
}

# Product Data
data = {
    "product": {
        "title": "Test listing - Apple Watch",
        "aspects": {
            "Feature": ["Water resistance", "GPS"],
            "CPU": ["Dual-Core Processor"]
        },
        "description": "Test listing - do not bid or buy",
        "upc": ["888462079525"],
        "imageUrls": [
            "http://store.storeimages.cdn-apple.com/4973/as-images.apple.com/is/image/AppleInc/aos/published/images/S/1/S1/42/S1-42-alu-silver-sport-white-grid?wid=332&hei=392"
        ]
    },
    "condition": "NEW",
    "packageWeightAndSize": {
        "dimensions": {
            "height": 5,
            "length": 10,
            "width": 15,
            "unit": "INCH"
        },
        "packageType": "MAILING_BOX",
        "weight": {
            "value": 2,
            "unit": "POUND"
        }
    },
    "availability": {
        "shipToLocationAvailability": {
            "quantity": 10
        }
    }
}

# API Request
response = requests.put(url, headers=headers, json=data)

try:
    data = response.json()
    print("JSON Response:", data)
except requests.exceptions.JSONDecodeError:
    print("❌ API returned invalid or empty response!")




url = "https://api.ebay.com/sell/inventory/v1/inventory_item"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept":"application/json",
    "Content-Type": "application/json",
    "Content-Language": "en-US"
}
params = {
    "limit": 50,   # Number of items per page
    "offset": 0    # Starting index
}

response = requests.get(url, headers=headers, params=params)
print("Status Code:", response.status_code)
print("Response:", response.json())

print("---------------------------------------Offer---------------------------------------")

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/abd00001"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    # "Accept":"application/json",
    "Content-Type": "application/json",
    # "Content-Language": "en-US"
}


response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.json())