import csv
import os
import requests
from PIL import Image
from io import BytesIO

# Settings
csv_file = "processor_details.csv"  # Path to your CSV file
folder = "downloaded_images"  # Folder to save images
output_format = "JPEG"  # Choose "JPEG" or "PNG"

# Create folder if it doesn't exist
os.makedirs(folder, exist_ok=True)

# Read CSV and download images
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=",")
    for row in reader:
        sku = row["sku"].strip()
        image_url = row["Image"].strip()
        
        if not image_url:
            continue  # Skip rows with empty URLs
        
        try:
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Convert to JPEG/PNG
            img = Image.open(BytesIO(response.content))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Save with SKU as the filename
            img.save(f"{folder}/{sku}.{output_format.lower()}", format=output_format)
            print(f"Downloaded: {sku}.{output_format.lower()}")
            
        except Exception as e:
            print(f"Failed to download {sku}: {e}")