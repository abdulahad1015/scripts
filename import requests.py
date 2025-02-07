import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

# Download NLTK data files (only need to run this once)
# nltk.download('punkt')
# nltk.download('stopwords')

def extract_keywords(urls):
    all_words = []  # Collect words across all URLs

    for url in urls:
        try:
            # Fetch the webpage
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            print(f"Fetching: {url}, Status Code: {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text
            text = soup.get_text()

            # Tokenize words
            words = word_tokenize(text)

            # Remove stopwords and non-alphabetic words
            stop_words = set(stopwords.words('english'))
            filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

            # Append filtered words to the main list
            all_words.extend(filtered_words)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    # Count word frequency across all URLs
    word_counts = Counter(all_words)

    # Get the top 30 keywords
    return word_counts.most_common(30)

# Example usage
urls = [
    "https://www.curemd.com/medical-billing-services",
    "https://www.247medicalbillingservices.com/",
    "https://verticaliq.com/product/medical-billing-services/",
    "https://www.tebra.com/billing-payments/managed-billing/"
]

output = extract_keywords(urls)
for keyword, count in output:
    print(f"{keyword}: {count}")
