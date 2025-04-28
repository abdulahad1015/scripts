import requests
import base64
import urllib.parse
import json
import os

# === CONFIGURATION ===
CLIENT_ID = 'AbdulAha-AbdulTes-PRD-f68cae849-84f8da57'
CLIENT_SECRET = 'PRD-68cae8493fb1-a76e-4550-b293-93a7'
RU_NAME = 'Abdul_Ahad-AbdulAha-AbdulT-dzmnnobqo'  # e.g. OsakaMotors_OsakaMotors-YourApp-xxxxx

SCOPES = [
    'https://api.ebay.com/oauth/api_scope/sell.account',
    'https://api.ebay.com/oauth/api_scope/sell.inventory',
    'https://api.ebay.com/oauth/api_scope/sell.fulfillment',
]

TOKEN_FILE = 'ebay_tokens.json'


def generate_auth_url():
    scope_str = urllib.parse.quote(' '.join(SCOPES))
    url = f"https://auth.ebay.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={RU_NAME}&scope={scope_str}"
    return url


def exchange_code_for_tokens(auth_code):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": RU_NAME
    }

    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        with open(TOKEN_FILE, "w") as f:
            json.dump(tokens, f, indent=2)
        print("✅ Tokens saved to ebay_tokens.json")
        return tokens
    else:
        print("❌ Failed to exchange code:", response.text)
        return None



def refresh_access_token(refresh_token):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": ' '.join(SCOPES)
    }

    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        print("🔁 Token refreshed and saved.")
        return tokens
    else:
        print("❌ Failed to refresh token:", response.text)
        return None


def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)


def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return None


def main():
    print("📌 eBay OAuth 2.0 Flow")

    tokens = load_tokens()
    if tokens:
        print("\n🟢 Existing tokens found.")
        choice = input("Refresh token (R) or Exit (E)? ").strip().lower()
        if choice == 'r':
            refresh_access_token(tokens['refresh_token'])
        return

    print("\n1. Open this URL in your browser:")
    print(generate_auth_url())

    auth_code = input("\n2. Paste the ?code=XXXX value from the redirect URL: ").strip()
    exchange_code_for_tokens(auth_code)


if __name__ == '__main__':
    main()
