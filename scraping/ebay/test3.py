import requests
import xmltodict
import json
import csv

# eBay API Credentials (Make sure to keep these secure!)
EBAY_API_ENDPOINT = "https://api.ebay.com/ws/api.dll"
EBAY_APP_ID = "AbdulAha-AbdulTes-PRD-f68cae849-84f8da57"
EBAY_DEV_ID = "2cf8d20b-824f-44fc-9968-76b113af2082"
EBAY_CERT_ID = "PRD-68cae8493fb1-a76e-4550-b293-93a7"
EBAY_USER_TOKEN = "v^1.1#i^1#f^0#I^3#r^1#p^3#t^Ul4xMF8xOkRCQUQ1RjBBNUI1RTg4MkE4QTNDRDFERTBCMjNGNjgwXzFfMSNFXjI2MA=="
ITEM_ID = "173770686984"

# Headers for API call
headers = {
    "X-EBAY-API-CALL-NAME": "GetItem",
    "X-EBAY-API-SITEID": "0",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "X-EBAY-API-DEV-NAME": EBAY_DEV_ID,
    "X-EBAY-API-APP-NAME": EBAY_APP_ID,
    "X-EBAY-API-CERT-NAME": EBAY_CERT_ID,
    "Content-Type": "text/xml"
}

# Request XML body
body = f"""<?xml version="1.0" encoding="utf-8"?>
<GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
  <RequesterCredentials>
    <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
  </RequesterCredentials>
  <ItemID>{ITEM_ID}</ItemID>
  <IncludeItemSpecifics>true</IncludeItemSpecifics>
  <DetailLevel>ReturnAll</DetailLevel>
</GetItemRequest>"""

# Make the API request
response = requests.post(EBAY_API_ENDPOINT, headers=headers, data=body)

if response.status_code == 200:
    # Convert XML to dict
    data_dict = xmltodict.parse(response.text)

    # Save raw response
    with open("item_details.xml", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Item details saved to 'item_details.xml'")

    # Extract and save variations
    try:
        variations = data_dict['GetItemResponse']['Item']['Variations']['Variation']
        # print(variations)
        extracted = []

        for var in variations:

            nv_list = var['VariationSpecifics']['NameValueList']
            if isinstance(nv_list, dict):
                nv_list = [nv_list]  # wrap single dict in a list

            spec = {nv['Name']: nv['Value'] for nv in nv_list}
            print(spec)
            extracted.append({
                
                "Price": var['StartPrice']['#text'] if isinstance(var['StartPrice'], dict) else var['StartPrice'],
                "Quantity": var['Quantity'],
                "Sold": var['SellingStatus']['QuantitySold'],
                "UPC": var.get("VariationProductListingDetails", {}).get("UPC", ""),
                **spec
            })

       
    except Exception as e:
        print("⚠️ Could not extract variations:", e)
else:
    print("❌ API call failed:", response.status_code)
    print(response.text)
