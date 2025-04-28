import requests

# Replace these values with your actual credentials and policy IDs
ACCESS_TOKEN = "v^1.1#i^1#r^1#p^3#I^3#f^0#t^Ul4xMF8xOjA2QzQ1RDgwRTZEREZDMTc3MzA1NkI5MzgxNTNCMjI2XzFfMSNFXjI2MA=="
SKU = "abd00001"  # Unique SKU for the item                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   a
MARKETPLACE_ID = "EBAY_US"
FULFILLMENT_POLICY_ID = "YOUR_FULFILLMENT_POLICY_ID"
PAYMENT_POLICY_ID = "YOUR_PAYMENT_POLICY_ID"
RETURN_POLICY_ID = "YOUR_RETURN_POLICY_ID"
PRICE = "299.99"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Content-Language": "en-US"
}

# Step 1: Add Inventory Item
inventory_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{SKU}"
inventory_data = {
    "product": {
        "title": "Test listing - Apple Watch",
        "aspects": {
            "CPU": ["Dual-Core Processor"],
            "Feature": ["Water resistance", "GPS"]
        },
        "description": "Test listing - do not bid or buy",
        "upc": ["888462079525"],
        "imageUrls": [
            "http://store.storeimages.cdn-apple.com/4973/as-images.apple.com/is/image/AppleInc/aos/published/images/S/1/S1/42/S1-42-alu-silver-sport-white-grid?wid=332&hei=392"
        ]
    },
    "condition": "NEW",
    "packageWeightAndSize": {
        "dimensions": {"width": 15.0, "length": 10.0, "height": 5.0, "unit": "INCH"},
        "packageType": "MAILING_BOX",
        "weight": {"value": 2.0, "unit": "POUND"}
    },
    "availability": {
        "shipToLocationAvailability": {"quantity": 10}
    }
}

response = requests.put(inventory_url, headers=HEADERS, json=inventory_data)
if response.status_code == 204:
    print("Inventory item added successfully!")
else:
    print("Error adding inventory item:", response.json())

# Step 2: Create Offer
offer_url = "https://api.ebay.com/sell/inventory/v1/offer"
offer_data = {
    "sku": SKU,
    "marketplaceId": MARKETPLACE_ID,
    "format": "FIXED_PRICE",
    "listingPolicies": {
        "fulfillmentPolicyId": FULFILLMENT_POLICY_ID,
        "paymentPolicyId": PAYMENT_POLICY_ID,
        "returnPolicyId": RETURN_POLICY_ID
    },
    "quantity": 10,
    "price": {
        "value": PRICE,
        "currency": "USD"
    }
}

response = requests.post(offer_url, headers=HEADERS, json=offer_data)
if response.status_code == 201:
    offer_id = response.json()["offerId"]
    print(f"Offer created successfully! Offer ID: {offer_id}")
else:
    print("Error creating offer:", response.json())
    exit()

# Step 3: Publish Offer
publish_url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish"
response = requests.post(publish_url, headers=HEADERS)

if response.status_code == 200:
    print("Offer published successfully! Your listing is live on eBay.")
else:
    print("Error publishing offer:", response.json())




url = "https://api.ebay.com/sell/account/v1/payment_policy"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "marketplaceId": MARKETPLACE_ID,
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.json())
