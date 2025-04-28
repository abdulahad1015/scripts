import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import csv
import time
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor , as_completed
import xmltodict




# Headers for API call
def load_ebay_credentials(filepath):
    creds = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                creds[key.strip()] = value.strip()
    return creds

def extract_item_id(url):
    return url.strip("/").split("/")[-1].split("?")[0]

EBAY_API_ENDPOINT = "https://api.ebay.com/ws/api.dll"
ITEM_ID = "311841532586"
credentials = load_ebay_credentials("ebay_credentials.txt")
EBAY_APP_ID = credentials['EBAY_APP_ID']
EBAY_DEV_ID = credentials['EBAY_DEV_ID']
EBAY_CERT_ID = credentials['EBAY_CERT_ID']
EBAY_USER_TOKEN = credentials['EBAY_USER_TOKEN']

class ScraperTab:
    def __init__(self, parent, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Scraper")
        self.input_file = None
        self.output_file = "ebay_scraped.csv"
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.executor = None
        self.lock = threading.Lock()

        # BooleanVars for multiple selections
        self.selected_options = {
            "Images": tk.BooleanVar(value=True),
            "Stock": tk.BooleanVar(value=True),
            "Description": tk.BooleanVar(value=True),
            "Shipping": tk.BooleanVar(value=True),
            "Versions": tk.BooleanVar(value=True),
            "Listing Ended": tk.BooleanVar(value=True)
        }

        self.checkButtons = []
        frame = tk.Frame(self.frame)
        frame.pack(padx=10, pady=10)

        self.select_btn = tk.Button(frame, text="Select CSV", command=self.select_file)
        self.select_btn.grid(row=0, column=1, padx=15, pady=5)

        self.file_label = tk.Label(frame, text="No file selected")
        self.file_label.grid(row=0, column=2, padx=15, pady=5)

        tk.Label(frame, text="Output File Name:").grid(row=1, column=1, padx=15, pady=5)
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.grid(row=1, column=2, padx=15, pady=5)
        self.output_entry.insert(0, self.output_file)

        col = 0
        for option, var in self.selected_options.items():
            button = tk.Checkbutton(frame, text=option, variable=var)
            button.grid(row=2, column=col, padx=5, pady=5)
            self.checkButtons.append(button)
            col += 1

        self.start_btn = tk.Button(frame, text="Start Scraping", command=self.start_scraping, state=tk.DISABLED)
        self.start_btn.grid(row=3, column=1, pady=5)

        self.pause_btn = tk.Button(frame, text="Pause", command=self.pause_scraping, state=tk.DISABLED)
        self.pause_btn.grid(row=3, column=2, pady=5)

        self.resume_btn = tk.Button(frame, text="Resume", command=self.resume_scraping, state=tk.DISABLED)
        self.resume_btn.grid(row=3, column=3, pady=5)

        self.log_box = scrolledtext.ScrolledText(self.frame, width=80, height=20)
        self.log_box.pack(padx=20, pady=10)

        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.eta_label = tk.Label(self.frame, text="ETA: Calculating...")
        self.eta_label.pack()

        self.progress_count_label = ttk.Label(self.frame, text="Completed: 0 / 0")
        self.progress_count_label.pack()

    def log(self, message):
        self.log_box.after(0, lambda: (self.log_box.insert(tk.END, message + "\n"), self.log_box.see(tk.END)))

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[["CSV files", "*.csv"]])
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.start_btn.config(state=tk.NORMAL)
            self.log(f"Selected file: {file_path}")


    def pause_scraping(self):
        self.pause_event.clear()
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.NORMAL)
        self.log("Scraping paused.")

    def resume_scraping(self):
        self.pause_event.set()
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.log("Resuming scraping...")

    def run_scraper(self):
        self.log("Starting scraper...")
        self.start_time = time.time()

        try:
            # Step 1: Read URLs early
            with open(self.input_file, "r", newline='', encoding="utf-8") as infile:
                rows = list(csv.reader(infile))

            if not rows:
                self.log("Error: CSV is empty.")
                return

            self.urls = [(row[0].strip(), row[1].strip()) for row in rows if len(row) >= 2]
            self.total_tasks = len(self.urls)
            self.progress["maximum"] = self.total_tasks
            self.progress["value"] = 0
            self.eta_label.config(text="ETA: Calculating...")

            # Step 2: Write header
            self.header = ["SKU", "URL", "Title", "Stock", "Price", "Auction", "Description", "Condition", "Shipping", "Versions", "Listing Ended"]
            image_columns = [f"Image_{i}" for i in range(1, 13)]
            self.header.extend(image_columns)

            with self.lock, open(self.output_file, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerow(self.header)


            # Step 4: Check progress
            def check_progress():
                done_count = sum(1 for f in futures if f.done())
                elapsed = time.time() - self.start_time

                if done_count > 0:
                    estimated_total = (elapsed / done_count) * self.total_tasks
                    eta = estimated_total - elapsed
                    eta_formatted = time.strftime("%H:%M:%S", time.gmtime(eta))
                else:
                    eta_formatted = "Calculating..."

                self.progress["value"] = done_count
                self.progress_count_label.config(text=f"Completed: {done_count} / {self.total_tasks}")
                self.eta_label.config(text=f"ETA: {eta_formatted}")

                if done_count < self.total_tasks:
                    self.frame.after(500, check_progress)
                else:
                    self.eta_label.config(text="Done!")

            # Step 3: Start scraping tasks
            futures = []
            self.executor = ThreadPoolExecutor(max_workers=10)

            for sku, url in self.urls:
                futures.append(self.executor.submit(self.scrape_and_write, sku, url, self.header))

            # Start tracking progress once
            self.frame.after(500, check_progress)

            # Wait for all tasks to complete
            for f in as_completed(futures):
                f.result()

        finally:
            self.executor.shutdown(wait=True)
            self.log("Scraping complete.")
            self.select_btn.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.DISABLED)
            self.output_entry.config(state=tk.NORMAL)

    def start_scraping(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return

        self.output_file = self.output_entry.get().strip()
        if not self.output_file.endswith(".csv"):
            self.output_file += ".csv"

        os.makedirs("ebay", exist_ok=True)
        self.output_file = os.path.join("ebay", self.output_file)

        self.pause_event.set()
        self.select_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        self.output_entry.config(state=tk.DISABLED)
        for button in self.checkButtons:
            button.config(state=tk.DISABLED)

        self.executor = ThreadPoolExecutor(max_workers=10)
        threading.Thread(target=self.run_scraper, daemon=True).start()
        


    def scrape_and_write(self, sku, url, header):
        selected = self.selected_options
        row_data = []
        scraped = {}
        
        while not self.pause_event.is_set():
            time.sleep(0.5)  # Sleep briefly while paused

        try:
            self.log(f"Processing SKU: {sku} | URL: {url}")
            response = requests.get(url, timeout=10, allow_redirects=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            scraped["Title"] = soup.find("h1").get_text(strip=True) if soup.find("h1") else "NA"

            if selected["Stock"].get():
                stock_div = soup.find(class_="x-quantity__availability")
                if stock_div:
                    spans = stock_div.find_all("span")
                    scraped["Stock"] = " ".join(span.get_text(strip=True) for span in spans) if spans else "NA"
                else:
                    scraped["Stock"] = "NA"
            else:
                scraped["Stock"] = "NA"

            scraped["Price"] = soup.find(class_="x-price-primary").get_text(strip=True) if soup.find(class_="x-price-primary") else "NA"

            if selected["Description"].get():
                desc_iframe = soup.find("iframe", id="desc_ifr")
                if desc_iframe:
                    try:
                        desc_url = desc_iframe["src"]
                        desc_response = requests.get(desc_url, timeout=10)
                        desc_response.raise_for_status()
                        desc_soup = BeautifulSoup(desc_response.content, "html.parser")
                        scraped["Description"] = desc_soup.get_text("\n", strip=True).replace(",", " ")[:32720]
                    except requests.exceptions.RequestException:
                        scraped["Description"] = "NA"
                else:
                    scraped["Description"] = "NA"
            else:
                scraped["Description"] = "NA"

            if selected["Shipping"].get():
                shipping_div = soup.find("div", class_="ux-labels-values col-12 ux-labels-values--shipping")
                if shipping_div:
                    content_div = shipping_div.find("div", class_="ux-labels-values__values-content")
                    if content_div:
                        spans = content_div.find_all("span")
                        scraped["Shipping"] = " ".join(span.get_text(strip=True) for span in spans) if spans else "NA"
                    else:
                        scraped["Shipping"] = "NA"
                else:
                    scraped["Shipping"] = "NA"
            else:
                scraped["Shipping"] = "NA"


            if selected["Listing Ended"].get():
                scraped["Listing Ended"] = any("This listing was ended" in text for text in soup.stripped_strings)
                if not scraped["Listing Ended"]:
                    sold_div = soup.find("div", class_="x-photos-min-view filmstrip filmstrip-x")
                    if sold_div:
                        cvip_div = sold_div.find("div", class_="x-photos-cvip")
                        if cvip_div:
                            span = cvip_div.find("span", class_="ux-textspans")
                            if span:
                                sold_text = span.get_text(strip=True)
                                scraped["Listing Ended"] = "True" if sold_text == "SOLD" else "NA"
                            else:
                                scraped["Listing Ended"] = "NA"
                        else:
                            scraped["Listing Ended"] = "NA"
                    else:
                        scraped["Listing Ended"] = "NA"
            else:
                scraped["Listing Ended"] = "NA"

            condition_div = soup.find("div", class_="x-item-condition-text")
            if condition_div:
                span = condition_div.find("span", class_="ux-textspans")
                scraped["Condition"] = span.get_text(strip=True) if span else "NA"
            else:
                scraped["Condition"] = "NA"

            scraped["Auction"] = "True" if soup.find("div", class_="vim x-bid-price") else "False"

            if selected["Images"].get():
                images = [img.get("data-src", "") for img in soup.find_all("img") if img.get("data-src")]
                scraped["Images"] = images[:12] + [""] * (12 - len(images))
            else:
                scraped["Images"] = [""] * 12

            if selected["Versions"].get():
                scraped["Versions"] = "True" if soup.find("div", class_="vim x-sku") else "NA"
                if scraped["Versions"] == "True":

                    item_id = extract_item_id(url)
                    headers = {
                        "X-EBAY-API-CALL-NAME": "GetItem",
                        "X-EBAY-API-SITEID": "0",
                        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
                        "X-EBAY-API-DEV-NAME": EBAY_DEV_ID,
                        "X-EBAY-API-APP-NAME": EBAY_APP_ID,
                        "X-EBAY-API-CERT-NAME": EBAY_CERT_ID,
                        "Content-Type": "text/xml"
                    }
                    body = f"""<?xml version="1.0" encoding="utf-8"?>
                    <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>{EBAY_USER_TOKEN}</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>{item_id}</ItemID>
                    <IncludeItemSpecifics>true</IncludeItemSpecifics>
                    <DetailLevel>ReturnAll</DetailLevel>
                    </GetItemRequest>"""
                    response = requests.post(EBAY_API_ENDPOINT, headers=headers, data=body)

                    if response.status_code == 200:
                        # Convert XML to dict
                        data_dict = xmltodict.parse(response.text)
                        # Extract and save variations
                        try:
                            variations = data_dict['GetItemResponse']['Item']['Variations']['Variation']
                            extracted = []
                            for var in variations:
                                nv_list = var['VariationSpecifics']['NameValueList']
                                if isinstance(nv_list, dict):
                                    nv_list = [nv_list]  # wrap single dict in a list

                                spec = {nv['Name']: nv['Value'] for nv in nv_list}
                                extracted.append({
                                    
                                    "Price": var['StartPrice']['#text'] if isinstance(var['StartPrice'], dict) else var['StartPrice'],
                                    "Quantity": var['Quantity'],
                                    "Sold": var['SellingStatus']['QuantitySold'],
                                    # "UPC": var.get("VariationProductListingDetails", {}).get("UPC", ""),
                                    **spec
                                })                        
                        except Exception as e:
                            print("⚠️ Could not extract variations:", e)
                    else:
                        print("❌ API call failed:", response.status_code)
                        print(response.text)
            else:
                scraped["Versions"] = "NA"

            # Construct row for writing
            row_data = [sku, url]
            for field in header[2:]:
                if field.startswith("Image_"):
                    row_data.extend(scraped.get("Images", [""] * 12))
                    break
                else:
                    row_data.append(scraped.get(field, "NA"))

            self.log(f"Scraped: {sku}")

        except requests.exceptions.RequestException as e:
            self.log(f"Network error for SKU {sku}: {e}")
            row_data = [sku, url] + ["Error: Network issue"] * (len(header) - 2)

        except Exception as e:
            self.log(f"Unexpected error for SKU {sku}: {e}")
            row_data = [sku, url] + ["Error: Unknown issue"] * (len(header) - 2)

        # Write the row data (whether success or error)
        try:
            with open(self.output_file, "a", newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerow(row_data)
                if scraped.get("Versions") == "True" and extracted:
                    writer.writerow(["Price","Quantity","Sold","Spec 1","Spec 2"])
                    for var in extracted:
                        writer.writerow(list(var.values()))
        except Exception as e:
            self.log(f"Failed to write CSV for SKU {sku}: {e}")




if __name__ == "__main__":
    root = tk.Tk()
    root.title("eBay Scraper Tool")
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    ScraperTab(root, notebook)
    tk.Button(root, text="Add New Scraper", command=lambda: ScraperTab(root, notebook)).pack()
    root.mainloop()
