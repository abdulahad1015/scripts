import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import csv
import time
import requests
from bs4 import BeautifulSoup
import os

class ScraperTab:
    def __init__(self, parent, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Scraper")
        self.input_file = None
        self.output_file = "ebay_scraped.csv"
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.scraping_thread = None
        self.last_processed_sku = None

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

        # Checkbuttons for attribute selection
        col = 0
        for option, var in self.selected_options.items():
            button = (tk.Checkbutton(frame, text=option, variable=var))
            button.grid(row=2, column=col, padx=5, pady=5)
            self.checkButtons.append(button)
            col += 1

        self.start_btn = tk.Button(frame, text="Start Scraping", command=self.start_scraping, state=tk.DISABLED)
        self.start_btn.grid(row=3, column=1, pady=5)

        self.pause_btn = tk.Button(frame, text="Pause Scraping", command=self.pause_scraping, state=tk.DISABLED)
        self.pause_btn.grid(row=3, column=2, pady=5)

        self.resume_btn = tk.Button(frame, text="Resume Scraping", command=self.resume_scraping, state=tk.DISABLED)
        self.resume_btn.grid(row=3, column=3, pady=5)

        self.log_box = scrolledtext.ScrolledText(self.frame, width=80, height=20)
        self.log_box.pack(padx=20, pady=10)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[["CSV files", "*.csv"]])
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.start_btn.config(state=tk.NORMAL)
            self.log(f"Selected file: {file_path}")

    def start_scraping(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select a CSV file first.")
            return

        self.output_file = self.output_entry.get().strip()
        if not self.output_file.endswith(".csv"):
            self.output_file += ".csv"

        try:
            os.makedirs("ebay", exist_ok=True)
            self.output_file = os.path.join("ebay", self.output_file)
        except OSError as e:
            self.log(f"Error creating output directory: {e}")
            return

        # Disable UI elements before starting
        self.pause_event.set()
        self.select_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.output_entry.config(state=tk.DISABLED)
        for button in self.checkButtons:
            button.config(state=tk.DISABLED)

        self.scraping_thread = threading.Thread(target=self.run_scraper, daemon=True)
        self.scraping_thread.start()

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
        # Define a constant header with all possible fields
        header = ["SKU", "URL", "Title", "Stock", "Price", "Description", "Shipping", "Versions", "Listing Ended"]
        image_columns = [f"Image_{i}" for i in range(1, 13)]
        header.extend(image_columns)  # Always include image columns

        selected = self.selected_options  # Get selected options

        # Ensure the CSV has the correct header
        try:
            file_exists = os.path.exists(self.output_file)
            with open(self.output_file, "a", newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                if not file_exists:  # Only write header if the file doesn't exist
                    writer.writerow(header)
        except Exception as e:
            self.log(f"Failed to write header to CSV: {e}")
            return

        start_time = time.time()
        total_count = 0

        try:
            with open(self.input_file, "r", newline='', encoding="utf-8") as infile:
                reader = csv.reader(infile)
                rows = list(reader)
                if not rows:
                    self.log("Error: The selected CSV file is empty.")
                    return

                for row in rows:
                    self.pause_event.wait(timeout=20)
                    if len(row) < 2:
                        self.log(f"Skipping invalid row: {row}")
                        continue

                    sku, url = row[0].strip(), row[1].strip()
                    self.log(f"Processing SKU: {sku} | URL: {url}")

                    try:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, "html.parser")
                        scraped = {}

                        # Extract data (ensure all fields exist in the output)
                        scraped["Title"] = soup.find("h1").get_text(strip=True) if soup.find("h1") else "NA"
                        
                        if selected["Stock"].get():
                            scraped["Stock"] = soup.find(class_="x-quantity__availability")if soup.find(class_="x-quantity__availability") else "NA"
                            if scraped["Stock"] != "NA":
                                scraped["Stock"] = scraped["Stock"].find_all("span") if scraped["Stock"].find_all("span") else "NA"
                                if scraped["Stock"] != "NA":
                                    stock="" 
                                    for span in scraped["Stock"]:
                                        stock=stock+span.get_text(strip=True)+" "
                                    scraped["Stock"] = stock if stock else "NA"

                        else:
                            scraped["Stock"] = "NA"
                        
                        scraped["Price"] = soup.find(class_="x-price-primary").get_text(strip=True) if soup.find(class_="x-price-primary") else "NA"

                        if selected["Description"].get():
                            desc_iframe = soup.find("iframe", id="desc_ifr") if soup.find("iframe", id="desc_ifr") else "NA"
                            if desc_iframe != "NA":
                                try:
                                    desc_url = desc_iframe["src"]
                                    desc_response = requests.get(desc_url, timeout=10)
                                    desc_response.raise_for_status()
                                    desc_soup = BeautifulSoup(desc_response.content, "html.parser")
                                    scraped["Description"] = desc_soup.get_text("\n", strip=True).replace(",", " ")[:32720] if desc_soup else "NA"
                                except requests.exceptions.RequestException:
                                    scraped["Description"] = "NA"
                        else:
                            scraped["Description"] = "NA"

                        
                        if selected["Shipping"].get():
                            shipping_div = soup.find("div",class_="ux-labels-values col-12 ux-labels-values--shipping") if soup.find("div",class_="ux-labels-values col-12 ux-labels-values--shipping") else "NA"
                            if shipping_div != "NA":
                                shipping_div = shipping_div.find("div", class_="ux-labels-values__values-content") if shipping_div.find("div", class_="ux-labels-values__values-content") else "NA"
                                if shipping_div != "NA":
                                    scraped["Shipping"] = shipping_div.find_all("span")[0].get_text().strip() if shipping_div and shipping_div.find_all("span") else "NA"
                                    if scraped["Shipping"] != "NA":
                                        shippiing_values = ""
                                        for span in shipping_div.find_all("span"):
                                            shippiing_values = shippiing_values + span.get_text().strip() + " "
                        else:
                            scraped["Shipping"] = "NA"

                        if selected["Versions"].get():
                            scraped["Versions"] = True if selected.get("Versions", False) and soup.find("div", class_="vim x-sku") else "NA"
                        else:
                            scraped["Versions"] = "NA"
                        
                        if selected["Listing Ended"].get():
                            scraped["Listing Ended"] = any("This listing was ended" in text for text in soup.stripped_strings) if selected.get("Listing Ended", False) else "NA"
                        else:
                            scraped["Listing Ended"] = "NA"
                        # Handle images (always store 12 image slots)
                        if selected["Images"].get():
                            images = [img.get("data-src", "") for img in soup.find_all("img") if img.get("data-src")]
                            scraped["Images"] = images[:12] + [""] * (12 - len(images))
                        else:
                            scraped["Images"] = [""] * 12  # Empty image slots if not selected

                        # Prepare row data, ensuring all columns exist
                        row_data = [sku, url]  # Start with SKU and URL
                        for field in header[2:]:  # Skip SKU and URL in the header
                            if field.startswith("Image_"):
                                row_data.extend(scraped.get("Images", [""] * 12))  # Add all 12 images
                                break
                            else:
                                row_data.append(scraped.get(field, "NA"))  # Use "NA" if missing

                        # Write data to CSV
                        try:
                            with open(self.output_file, "a", newline='', encoding='utf-8') as outfile:
                                writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                                writer.writerow(row_data)
                        except Exception as e:
                            self.log(f"Failed to write row to CSV: {e}")
                            continue

                        self.log(f"Scraped: {sku}")
                        total_count += 1
                    except requests.exceptions.RequestException as e:
                        self.log(f"Network error for SKU {sku}: {e}")
                        continue
        except Exception as e:
            self.log(f"Failed to process file: {e}")

        elapsed = time.time() - start_time
        self.log(f"Scraping complete. Total items scraped: {total_count}")
        self.log(f"Time taken: {elapsed:.2f} seconds")

        # Re-enable UI elements after scraping
        self.select_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.resume_btn.config(state=tk.DISABLED)
        self.output_entry.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("eBay Scraper Tool")# pyinstaller --onefile --windowed --name "EbayScraper" ebay_scraper.py
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    ScraperTab(root, notebook)
    tk.Button(root, text="Add New Scraper", command=lambda: ScraperTab(root, notebook)).pack()
    root.mainloop()
