import pdfplumber
import pandas as pd
import re

pdf_path = "C:\\Users\\Osaka Motors\\Downloads\\pdfs\\july.pdf"
csv_output_path = "transactions.csv"

transactions = []
current_transaction = None

def is_noise(line):
    # Define keywords for non-transaction lines
    noise_keywords = ["POSTING DATE", "DESCRIPTION", "AMOUNT", "Subtotal", "Service Charges", "MAINTENANCE FEE", "Page:", "Statement Period", "Call 1-800"]
    return any(keyword in line for keyword in noise_keywords)

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if is_noise(line):
                continue

            # Check if line starts with a date (e.g., "07/08")
            date_match = re.match(r"^(\d{2}/\d{2})\s+(.+)", line)
            if date_match:
                if current_transaction and current_transaction.get("Amount"):
                    transactions.append(current_transaction)
                current_transaction = {
                    "Date": date_match.group(1),
                    "Description": date_match.group(2).strip(),
                    "Amount": ""
                }
                continue

            # Check if line is a standalone amount
            amount_match = re.match(r"^\s*(\d+\.\d{2})\s*$", line)
            if amount_match and current_transaction is not None:
                current_transaction["Amount"] = amount_match.group(1)
                transactions.append(current_transaction)
                current_transaction = None
                continue

            # Append line to description if it doesn't trigger any of the above
            if current_transaction is not None:
                current_transaction["Description"] += " " + line

if current_transaction is not None and current_transaction.get("Amount"):
    transactions.append(current_transaction)

df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])
df.to_csv(csv_output_path, index=False)

print(f"✅ Transactions extracted: {len(transactions)}")
print(f"Saved to: {csv_output_path}")
