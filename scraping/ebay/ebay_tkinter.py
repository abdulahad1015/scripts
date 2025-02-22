import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import csv
import time
import requests
from bs4 import BeautifulSoup
import os
# pyinstaller --onefile --windowed --name "EbayScraper" ebay_scraper.py

def append_to_csv(data, filename="ebay/ebay_scraped.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

class EbayScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eBay Scraper Tool")
        self.input_file = None
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)
        self.select_btn = tk.Button(frame, text="Select CSV", command=self.select_file)
        self.select_btn.grid(row=0, column=0, padx=5, pady=5)
        self.file_label = tk.Label(frame, text="No file selected")
        self.file_label.grid(row=0, column=1, padx=5, pady=5)
        self.start_btn = tk.Button(frame, text="Start Scraping", command=self.start_scraping, state=tk.DISABLED)
        self.start_btn.grid(row=1, column=0, columnspan=2, pady=5)
        self.log_box = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_box.pack(padx=10, pady=10)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.start_btn.config(state=tk.NORMAL)
            self.log(f"Selected file: {file_path}")

    def start_scraping(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return
        self.select_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.run_scraper, daemon=True).start()

    def run_scraper(self):
        start_time = time.time()
        total_count = 0
        try:
            with open(self.input_file, "r", newline='', encoding="utf-8") as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if len(row) < 2:
                        self.log(f"Skipping invalid row: {row}")
                        continue
                    sku, url = row[0].strip(), row[1].strip()
                    self.log(f"Processing SKU: {sku} | URL: {url}")
                    try:
                        response = requests.get(url)
                        soup = BeautifulSoup(response.content, "html.parser")
                        error_tag = soup.find("p", class_="error-header-v2__title")
                        if error_tag:
                            error_text = error_tag.get_text().strip()
                            self.log(f"Error: {error_text} for SKU: {sku}")
                            out_row = (sku, "NA", "Item not found", "NA", "NA", url)
                            append_to_csv(out_row)
                            continue
                        title_tag = soup.find("h1")
                        if title_tag and title_tag.find("span"):
                            title = title_tag.find("span").get_text().strip()
                        else:
                            title = "NA"
                        quantity_div = soup.find("div", class_="x-quantity__availability")
                        if quantity_div and quantity_div.find("span"):
                            stock = quantity_div.find("span").get_text().strip()
                        else:
                            stock = "NA"
                        price_div = soup.find("div", class_="x-price-primary")
                        if price_div and price_div.find("span"):
                            price = price_div.find("span").get_text(strip=True)
                        else:
                            price = "NA"
                        shipping_div = soup.find("div", class_="ux-labels-values__values col-9")
                        if shipping_div:
                            shipping_spans = shipping_div.find_all("span")
                            shipping = shipping_spans[0].get_text().strip() if shipping_spans else "NA"
                        else:
                            shipping = "NA"
                        out_row = (sku, title, stock, price, shipping, url)
                        append_to_csv(out_row)
                        self.log(f"Scraped: {out_row}")
                        total_count += 1
                    except Exception as e:
                        self.log(f"An error occurred with SKU {sku}: {e}")
                        time.sleep(30)
            elapsed = time.time() - start_time
            self.log(f"Finished scraping {total_count} items in {elapsed:.2f} seconds.")
        except Exception as e:
            self.log(f"Failed to process file: {e}")
        self.select_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = EbayScraperApp(root)
    root.mainloop()
