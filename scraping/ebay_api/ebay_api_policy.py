import requests

# Replace with your eBay OAuth token
ACCESS_TOKEN = "v^1.1#i^1#f^0#r^0#p^3#I^3#t^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"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# eBay API Endpoint
EBAY_API_URL = "https://api.ebay.com/sell/account/v1"

# Marketplace ID (Change based on your country, e.g., "EBAY_UK", "EBAY_DE")
MARKETPLACE_ID = "EBAY_US"

# Create a Payment Policy
payment_policy = {
    "name": "Default Payment Policy",
    "marketplaceId": MARKETPLACE_ID,
    "paymentMethods": [{"paymentMethodType": "CREDIT_CARD"}]
}

# Create a Return Policy
return_policy = {
    "name": "Default Return Policy",
    "marketplaceId": MARKETPLACE_ID,
    "returnsAccepted": True,
    "returnPeriod": {"unit": "DAY", "value": 30},
    "refundMethod": "MONEY_BACK",
    "returnShippingCostPayer": "BUYER"
}

# Create a Fulfillment (Shipping) Policy
shipping_policy = {
    "name": "Default Shipping Policy",
    "marketplaceId": MARKETPLACE_ID,
    "shippingOptions": [{
        "costType": "FLAT_RATE",
        "shippingServices": [{
            "shippingServiceCode": "USPSPriority",
            "shippingCost": {"value": "5.00", "currency": "USD"}
        }]
    }]
}

# Function to create policy
def create_policy(policy_type, data):
    url = f"{EBAY_API_URL}/{policy_type}_policy"
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        print(f"{policy_type.capitalize()} Policy Created Successfully!")
        print("Response:", response.json())
    else:
        print(f"Error Creating {policy_type.capitalize()} Policy:")
        print(response.json())

# Create all policies
create_policy("payment", payment_policy)
create_policy("return", return_policy)
create_policy("fulfillment", shipping_policy)
