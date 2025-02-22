import json
import os
from datetime import datetime
from seleniumbase import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time,csv,requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configuration
LOG_FILE = "m4l/memory/links_progress2.csv"
JSON_FILE = "m4l/memory/products2.json"
MAX_RETRIES = 3
folder = "m4l/memory/images"  # Folder to save images
output_format = "JPEG"  # Choose "JPEG" or "PNG"


CPU_LINKS= [
    # ("Memory By Brand", "Cisco Memory", "https://m4l.com/cisco-memory-upgrades"),
    # ("Memory By Brand", "Crucial Memory", "https://m4l.com/crucial-memory-upgrades"),
    # ("Memory By Brand", "Dell Memory", "https://m4l.com/dell-memory-upgrades"),
    # ("Memory By Brand", "HP Memory", "https://m4l.com/hp-memory-upgrades"),
    # ("Memory By Brand", "Hynix Memory", "https://m4l.com/hynix-memory-upgrades"),
    # ("Memory By Brand", "IBM Memory", "https://m4l.com/ibm-memory-upgrades"),
    # ("Memory By Brand", "Kingston Memory", "https://m4l.com/kingston-memory-upgrades"),
    # ("Memory By Brand", "Micron Memory", "https://m4l.com/micron-memory-upgrades"),
    # ("Memory By Brand", "Oracle Memory", "https://m4l.com/oracle-memory-upgrades"),
    # ("Memory By Brand", "Samsung Memory", "https://m4l.com/samsung-memory-upgrades"),
    ("Memory By Brand", "Sun Memory", "https://m4l.com/sun-memory-upgrades"),

    ("Memory By Capacity", "256GB Memory", "https://m4l.com/256gb-memory-upgrades"),
    ("Memory By Capacity", "128GB Memory", "https://m4l.com/128gb-memory-upgrades"),
    ("Memory By Capacity", "64GB Memory", "https://m4l.com/64gb-memory-upgrades"),
    ("Memory By Capacity", "32GB Memory", "https://m4l.com/32gb-memory-upgrades"),
    ("Memory By Capacity", "16GB Memory", "https://m4l.com/16gb-memory-upgrades"),
    ("Memory By Capacity", "8GB Memory", "https://m4l.com/8gb-memory-upgrades"),
    ("Memory By Capacity", "4GB Memory", "https://m4l.com/4gb-memory-upgrades"),
    ("Memory By Capacity", "2GB Memory", "https://m4l.com/2gb-memory-upgrades"),
    ("Memory By Capacity", "1GB Memory", "https://m4l.com/1gb-memory-upgrades"),

    ("Memory By Category", "Server Memory", "https://m4l.com/server-memory-upgrades"),
    ("Memory By Category", "Laptop Memory", "https://m4l.com/laptop-memory-upgrades"),
    ("Memory By Category", "Desktop Memory", "https://m4l.com/desktop-memory-upgrades"),
    ("Memory By Category", "Gaming Memory", "https://m4l.com/gaming-memory-upgrades"),

    ("Memory By Bus Type", "DDR4-3200MHz", "https://m4l.com/pc-25600-ddr4-3200mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR4-2933MHz", "https://m4l.com/pc-23400-ddr4-2933mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR4-2666MHz", "https://m4l.com/pc-21300-ddr4-2666mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR4-2400MHz", "https://m4l.com/pc-19200-ddr4-2400mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR4-2133MHz", "https://m4l.com/pc-17000-ddr4-2133mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR3-1866MHz", "https://m4l.com/pc-14900-ddr3-1866mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR3-1600MHz", "https://m4l.com/pc-12800-ddr3-1600mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR3-1333MHz", "https://m4l.com/pc-10600-ddr3-1333mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR3-1066MHz", "https://m4l.com/pc-8500-ddr3-1066mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR2-800MHz", "https://m4l.com/pc-6400-ddr2-800mhz-memory-upgrades"),
    ("Memory By Bus Type", "DDR2-667MHz", "https://m4l.com/pc-5300-ddr2-667mhz-memory-upgrades"),

    ("Memory By Type", "DDR4 LRDIMM", "https://m4l.com/ddr4-lrdimm-memory-upgrades"),
    ("Memory By Type", "DDR3 LRDIMM", "https://m4l.com/ddr3-lrdimm-memory-upgrades"),
    ("Memory By Type", "DDR4 SDRAM", "https://m4l.com/ddr4-sdram-memory-upgrades"),
    ("Memory By Type", "DDR3 SDRAM", "https://m4l.com/ddr3-sdram-memory-upgrades"),
    ("Memory By Type", "DDR2 SDRAM", "https://m4l.com/ddr2-sdram-memory-upgrades"),
    ("Memory By Type", "DDR2 Fully Buffered", "https://m4l.com/ddr2-fully-buffered-memory-upgrades"),
    ("Memory By Type", "DDR1 SDRAM", "https://m4l.com/ddr1-sdram-memory-upgrades"),
    ("Memory By Type", "DDR4 SoDimm", "https://m4l.com/ddr4-sodimm-memory-upgrades"),
    ("Memory By Type", "DDR3 SoDimm", "https://m4l.com/ddr3-sodimm-memory-upgrades"),
    ("Memory By Type", "DDR2 SoDimm", "https://m4l.com/ddr2-sodimm-memory-upgrades"),
]

def init_log():
    """Initialize log file with headers if it doesn't exist"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "status", "category", "brand", "model", "url", "message"])

def log_progress(status, category, brand, model, url, message=""):
    """Append progress to the log file atomically"""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            status,
            category,
            brand if brand else "",
            model if model else "",
            url,
            message
        ])
def get_processing_state(target_url):
    """Retrieve the processing state from the log file."""
    state = {
        "pages_processed": False,
        "current_page": None,
        "product_urls": set(),  # Use set to avoid duplicates
        "completed_products": set()
    }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header
            for row in reader:
                if row[5] == target_url:  # Check if it's the correct URL
                    if row[1] == "pages_processed":
                        state["pages_processed"] = True
                    elif row[1] == "page_marker":
                        state["current_page"] = row[6]
                    elif row[1] == "product_found":
                        state["product_urls"].add(row[6])
                    elif row[1] == "completed_product":
                        state["completed_products"].add(row[5])  # Fix: Use row[5] as product URL

    except FileNotFoundError:
        pass  # Fresh run

    return state



def scrape_product_page(driver, url, link):
    """Scrape detailed product information with improved selectors"""
    try:
        # driver.execute_script("window.focus();")
        driver.get(url)
        # time.sleep(3)  # Allow more time for loading
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Base information
        product_data = {
            "Part No":"N/A",
            "category": link[0],
            "subcategory": link[1] if len(link) > 1 else "",
            "brand": link[2] if len(link) > 2 else link[1] if "Brand" in link[0] else "",
            "model": link[3] if len(link) > 3 else link[2] if len(link) > 2 else "",
            "product_url": url,
            "title": get_text(soup.find("h1")) or "N/A",
            "price": "N/A",
            "specifications": {},
            "description": "N/A",
            "images": [],
            "stock_status": "N/A"
        }

        # Price (try multiple selectors)
        product_data["price"] = soup.find("span", class_="discounted-price").get_text(strip=True) if soup.find("span", class_="discounted-price") else "NA"
        product_data["Part No"] = soup.find("h2", class_="mpn-value").get_text(strip=True) if soup.find("h2", class_="mpn-value") else "NA"


        rows = soup.find_all("tr")
        # print(rows)
        for row in rows:
            columns=row.find_all("td")
            if len(columns) == 2:
                key = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                product_data["specifications"][key] = value

        # Description (multi-section support)
        description_parts = []
        for desc_selector in [".product-description", ".details-content"]:
            if desc_section := soup.select_one(desc_selector):
                description_parts.append(desc_section.get_text("\n", strip=True))
        product_data["description"] = "\n\n".join(description_parts) or "N/A"

        #Images
        if soup.find("div" , class_="m4l-item-image"):
            images=soup.find("div" , class_="m4l-item-image")
            if (images.find("img").get("src")):
                image_link=images.find("img").get("src")
                product_data["images"].append(image_link)
                download_image(product_data["Part No"],image_link)
        
        # Stock status
        stock_selectors = [
            ".stock-status",
            ".inventory span",
            "[data-product-stock]"
        ]
        for selector in stock_selectors:
            if stock_element := soup.select_one(selector):
                product_data["stock_status"] = stock_element.get_text(strip=True)
                break

        return product_data

    except Exception as e:
        # print(f"Error scraping {url}: {str(e)}")
        return None

def get_text(element):
    """Safe text extraction helper"""
    return element.get_text(strip=True) if element else ""

def save_to_json(data):
    """Append product data to JSON lines file"""
    with open(JSON_FILE, "a", encoding="utf-8") as f:
        json_line = json.dumps(data, ensure_ascii=False)
        f.write(json_line + "\n")

def get_last_position(target_url):
    """Get processing status with proper defaults"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            relevant = [row for row in reader if row["url"] == target_url]
            
            if not relevant:
                return ("new", [])
                
            # Get all collected product URLs
            product_urls = [row["url"] for row in relevant 
                          if row["status"] == "product_found"]
            
            if any(row["status"] == "completed" for row in relevant):
                return ("completed", [])
                
            return ("in_progress", product_urls)
            
    except FileNotFoundError:
        return ("new", [])

def process_link(link):
    """Process product pages and resume from last saved state."""
    base_url = link[-1]
    state = get_processing_state(base_url)

    if state["pages_processed"]:
        print(f"Skipping page collection for: {base_url}")
    else:
        print(f"Starting page collection for: {base_url}")

    driver = Driver(uc=True, headless=False)
    driver.maximize_window()

    try:
        # Resume from last known page
        current_page = state["current_page"] or f"{base_url}?pg=1&sz=40"
        
        if not state["pages_processed"]:
            while True:
                log_progress("page_marker", *link[:-1], "PAGE_PROGRESS:"+base_url, current_page)

                driver.get(current_page)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.m4l-grid-view"))
                )

                # Extract products
                soup = BeautifulSoup(driver.page_source, "html.parser")
                new_urls = [
                    (a["href"] if a["href"].startswith("http") else f"https://www.m4l.com{a['href']}")
                    for a in soup.select("li.m4l-grid-view div.m4l-item-title a")
                ]

                for url in new_urls:
                    if url not in state["product_urls"]:
                        log_progress("product_found", *link[:-1], base_url, url)
                        state["product_urls"].add(url)

                # Find next page
                try:
                    next_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.arrow:last-child:not(.unavailable)"))
                    )
                    current_page = next_btn.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    log_progress("pages_processed", *link[:-1], base_url, "Page collection complete")
                    break

        # **Remove already completed products from processing list**
        remaining_products = [url for url in state["product_urls"] if url not in state["completed_products"]]
        total_products = len(state["product_urls"])
        print(f"Resuming with {len(remaining_products)}/{total_products} products remaining")

        for idx, url in enumerate(remaining_products, 1):
            print(f"[{idx}/{total_products}] Processing: {url}")

            for attempt in range(MAX_RETRIES):
                try:
                    data = scrape_product_page(driver, url, link)
                    if data:
                        save_to_json(data)
                        log_progress("completed_product", *link[:-1], url, "Product completed")
                        break
                except Exception as e:
                    if attempt == MAX_RETRIES - 1:
                        print(f"Permanent failure on {url}: {str(e)}")
                        log_progress("error", *link[:-1], url, f"Failed after {MAX_RETRIES} attempts")

        # Final completion
        log_progress("completed", *link[:-1], base_url, "All products processed")

    finally:
        driver.quit()

def get_log_entries(target_url):
    """Get all log entries for a specific URL"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row for row in reader if row["url"] == target_url]
    except FileNotFoundError:
        return []







#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------


def download_image(sku, image_url):
    try:
        # Handle relative URLs
        if not image_url.startswith(("http://", "https://")):
            image_url = f"https://www.m4l.com{image_url}"
            
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Create image directory if needed
        os.makedirs(folder, exist_ok=True)
        
        # Convert to JPEG/PNG
        img = Image.open(BytesIO(response.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Save with SKU as the filename
        img.save(f"{folder}/{sku}.{output_format.lower()}", format=output_format)
        print(f"Downloaded: {sku}.{output_format.lower()}")
            
    except Exception as e:
        print(f"Failed to download {sku}: {e}")

def main():
    init_log()
    os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
    os.makedirs(folder, exist_ok=True)  # Create image folder
    
    for link in CPU_LINKS:
        if os.path.exists("STOP.txt"):  # Emergency stop file
            print("Stop file detected, exiting...")
            break
        try:
            process_link(link)
        except Exception as e:
            print(f"Error processing link {link}: {str(e)}")
            continue

if __name__ == "__main__":
    main()