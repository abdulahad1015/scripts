import pdfplumber
import pandas as pd
import re

# Path to your PDF file
pdf_path = "C:\\Users\\Osaka Motors\\Downloads\\pdfs\\july.pdf"
csv_output_path = "transactions.csv"

transactions = []

with pdfplumber.open(pdf_path) as pdf:
    capture = False
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        
        for line in lines:
            if "DAILY ACCOUNT ACTIVITY" in line:
                capture = True  # Start capturing transactions
            elif "DAILY BALANCE SUMMARY" in line:
                capture = False  # Stop capturing transactions
            
            if capture:
                match = re.match(r"(\d{2}/\d{2})\s+(.+?)\s+(\d+\.\d{2})$", line)
                if match:
                    date, description, amount = match.groups()
                    transactions.append([date, description.strip(), amount])

# Convert to DataFrame
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

# Save to CSV
df.to_csv(csv_output_path, index=False)

print(f"Transactions extracted and saved to: {csv_output_path}")
