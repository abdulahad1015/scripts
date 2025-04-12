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
            "Images": tk.BooleanVar(value=False),
            "Title": tk.BooleanVar(value=True),
            "Stock": tk.BooleanVar(value=False),
            "Price": tk.BooleanVar(value=False),
            "Description": tk.BooleanVar(value=False)
        }

        frame = tk.Frame(self.frame)
        frame.pack(padx=10, pady=10)

        self.select_btn = tk.Button(frame, text="Select CSV", command=self.select_file)
        self.select_btn.grid(row=0, column=1, padx=5, pady=5)

        self.file_label = tk.Label(frame, text="No file selected")
        self.file_label.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Output File Name:").grid(row=1, column=1, padx=5, pady=5)
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.grid(row=1, column=2, padx=5, pady=5)
        self.output_entry.insert(0, self.output_file)

        # Checkbuttons for attribute selection
        col = 0
        for option, var in self.selected_options.items():
            tk.Checkbutton(frame, text=option, variable=var).grid(row=2, column=col, padx=5, pady=5)
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
        # Define order for header output
        order = ["Images", "Title", "Stock", "Price", "Description"]
        selected = {opt: var.get() for opt, var in self.selected_options.items()}
        header = ["SKU"]
        for opt in order:
            if selected.get(opt, False):
                if opt == "Images":
                    header.extend([f"Image_{i}" for i in range(1, 13)])
                else:
                    header.append(opt)
        header.append("URL")

        start_time = time.time()
        total_count = 0

        try:
            with open(self.input_file, "r", newline='', encoding="utf-8") as infile:
                reader = csv.reader(infile)
                rows = list(reader)
                if not rows:
                    self.log("Error: The selected CSV file is empty.")
                    return

                # Write header if output file doesn't exist
                if not os.path.exists(self.output_file):
                    with open(self.output_file, "w", newline='', encoding='utf-8') as outfile:
                        writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        writer.writerow(header)

                for row in rows:
                    self.pause_event.wait(timeout=60)
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

                        if selected.get("Title", False):
                            scraped["Title"] = soup.find("h1").get_text(strip=True) if soup.find("h1") else "NA"
                        if selected.get("Stock", False):
                            scraped["Stock"] = soup.find(class_="x-quantity__availability").get_text(strip=True) if soup.find(class_="x-quantity__availability") else "NA"
                        if selected.get("Price", False):
                            scraped["Price"] = soup.find(class_="x-price-primary").get_text(strip=True) if soup.find(class_="x-price-primary") else "NA"
                        if selected.get("Description", False):
                            desc_iframe = soup.find("iframe", id="desc_ifr")
                            if desc_iframe:
                                try:
                                    desc_url = desc_iframe["src"]
                                    desc_response = requests.get(desc_url, timeout=10)
                                    desc_response.raise_for_status()
                                    desc_soup = BeautifulSoup(desc_response.content, "html.parser")
                                    scraped["Description"] = desc_soup.get_text("\n", strip=True)[:32720] if desc_soup else "NA"
                                    
                                except requests.exceptions.RequestException as e:
                                    self.log(f"Failed to fetch description for SKU {sku}: {e}")
                                    scraped["Description"] = "NA"
                        if selected.get("Images", False):
                            images = [img.get("data-src", "") for img in soup.find_all("img") if img.get("data-src")]
                            scraped["Images"] = images[:12] + [""] * (12 - len(images))

                        # Build row data based on header order
                        row_data = [sku]
                        for opt in order:
                            if selected.get(opt, False):
                                if opt == "Images":
                                    row_data.extend(scraped.get("Images", [""] * 12))
                                else:
                                    row_data.append(scraped.get(opt, "NA"))
                        row_data.append(url)

                        with open(self.output_file, "a", newline='', encoding='utf-8') as outfile:
                            writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                            writer.writerow(row_data)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("eBay Scraper Tool")
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    ScraperTab(root, notebook)
    tk.Button(root, text="Add New Scraper", command=lambda: ScraperTab(root, notebook)).pack()
    root.mainloop()


