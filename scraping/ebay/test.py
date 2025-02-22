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
        
        frame = tk.Frame(self.frame)
        frame.pack(padx=10, pady=10)
        
        self.select_btn = tk.Button(frame, text="Select CSV", command=self.select_file)
        self.select_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.file_label = tk.Label(frame, text="No file selected")
        self.file_label.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Output File Name:").grid(row=1, column=0, padx=5, pady=5)
        self.output_entry = tk.Entry(frame, width=30)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        self.output_entry.insert(0, self.output_file)

        self.start_btn = tk.Button(frame, text="Start Scraping", command=self.start_scraping, state=tk.DISABLED)
        self.start_btn.grid(row=2, column=0, pady=5)
        
        self.pause_btn = tk.Button(frame, text="Pause Scraping", command=self.pause_scraping, state=tk.DISABLED)
        self.pause_btn.grid(row=2, column=1, pady=5)
        
        self.resume_btn = tk.Button(frame, text="Resume Scraping", command=self.resume_scraping, state=tk.DISABLED)
        self.resume_btn.grid(row=2, column=2, pady=5)
        
        self.log_box = scrolledtext.ScrolledText(self.frame, width=80, height=20)
        self.log_box.pack(padx=10, pady=10)

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
        self.output_file = os.path.join("ebay", self.output_file)
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        self.pause_event.set()
        self.select_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
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
        start_time = time.time()
        total_count = 0
        try:
            with open(self.input_file, "r", newline='', encoding="utf-8") as infile:
                reader = csv.reader(infile)
                resume = False if self.last_processed_sku is None else True
                for row in reader:
                    self.pause_event.wait()
                    if len(row) < 2:
                        self.log(f"Skipping invalid row: {row}")
                        continue
                    sku, url = row[0].strip(), row[1].strip()
                    if resume:
                        if sku == self.last_processed_sku:
                            resume = False
                        continue
                    self.last_processed_sku = sku
                    self.log(f"Processing SKU: {sku} | URL: {url}")
                    try:
                        response = requests.get(url)
                        soup = BeautifulSoup(response.content, "html.parser")
                        error_tag = soup.find("p", class_="error-header-v2__title")
                        if error_tag:
                            error_text = error_tag.get_text().strip()
                            self.log(f"Error: {error_text} for SKU: {sku}")
                            out_row = (sku, "NA", "Item not found", "NA", "NA", url)
                        else:
                            title = soup.find("h1").find("span").get_text().strip() if soup.find("h1") and soup.find("h1").find("span") else "NA"
                            stock = soup.find("div", class_="x-quantity__availability").find("span").get_text().strip() if soup.find("div", class_="x-quantity__availability") and soup.find("div", class_="x-quantity__availability").find("span") else "NA"
                            price = soup.find("div", class_="x-price-primary").find("span").get_text(strip=True) if soup.find("div", class_="x-price-primary") and soup.find("div", class_="x-price-primary").find("span") else "NA"
                            versions = soup.find("div", class_="vim x-sku") if soup.find("div", class_="vim x-sku") else None
                            if versions:
                                versions = True
                            else:
                                versions = False
                            
                            shipping_div = soup.find("div", class_="ux-labels-values__values col-9")
                            shipping = shipping_div.find_all("span")[0].get_text().strip() if shipping_div and shipping_div.find_all("span") else "NA"
                            listing_ended_flag = any("This listing was ended" in text for text in soup.stripped_strings)

                            # description_div = soup.find("div", {"id": "viTabs_0_is"})  # Adjust if needed
                            # if description_div:
                            #     description=description_div.get_text("\n", strip=True)  # Keeps line breaks
                            # else:
                            #     return "Description not found."
                            desc_iframe = soup.find("iframe", id="desc_ifr")
                            if desc_iframe:
                                desc_url = desc_iframe.get("src")
                                desc_response = requests.get(desc_url)
                                desc_soup = BeautifulSoup(desc_response.content, "html.parser")
                                description = desc_soup.get_text("\n", strip=True)
                            else:
                                description = "NA"
                            images = soup.find_all("img")
                            image_url = [""]*12
                            for image in images:
                                if image.get("data-idx"):
                                    if int(image.get("data-idx")) >= 0 and int(image.get("data-idx")) < 12:
                                        image_url[int(image.get("data-idx"))]=image.get("data-src")
                            out_row = (sku, title, stock,listing_ended_flag ,price,versions,shipping,description ,url, image_url[0], image_url[1], image_url[2], image_url[3], image_url[4], image_url[5], image_url[6], image_url[7], image_url[8], image_url[9], image_url[10], image_url[11])
                        with open(self.output_file, "a", newline='', encoding='utf-8') as outfile:
                            writer = csv.writer(outfile)
                            writer.writerow(out_row)
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