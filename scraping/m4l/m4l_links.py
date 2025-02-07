import csv
import os
from time import sleep
from datetime import datetime
from seleniumbase import Driver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

# Configuration
LOG_FILE = "m4l/processors/links_progress.csv"
CPU_LINKS = (("CPU By Socket", "AMD", "Socket AM2", "https://m4l.com/amd-socketam2-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket AM2+", "https://m4l.com/amd-socketam2plus-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket AM3", "https://m4l.com/amd-socketam3-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket AM3+", "https://m4l.com/amd-socketam3plus-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket AM4", "https://m4l.com/amd-socketam4-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket FM1", "https://m4l.com/amd-socketfm1-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket FM2", "https://m4l.com/amd-socketfm2-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket FM2+", "https://m4l.com/amd-socketfm2plus-cpu-processors"),
    ("CPU By Socket", "AMD", "Socket G34", "https://m4l.com/amd-socketg34-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 1150", "https://m4l.com/intel-lga1150-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 1151", "https://m4l.com/intel-lga1151-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 1155", "https://m4l.com/intel-lga1155-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 1366", "https://m4l.com/intel-lga1366-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 2011", "https://m4l.com/intel-lga2011-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 2011 V3", "https://m4l.com/intel-lga2011-v3-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 2066", "https://m4l.com/intel-lga2066-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 3647", "https://m4l.com/intel-lga3647-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 771", "https://m4l.com/intel-lga771-cpu-processors"),
    ("CPU By Socket", "Intel", "LGA 775", "https://m4l.com/intel-lga775-cpu-processors"),
    ("CPU By Category",  "Server CPU", "https://m4l.com/xeon-server-cpu-processors"),
    ("CPU By Category",  "Desktop CPU", "https://m4l.com/desktop-cpu-processors"),
    ("CPU By Category",  "Mobile CPU", "https://m4l.com/mobile-cpu-processors"),
    ("CPU By Brand", "AMD CPU", "https://m4l.com/amd-cpu-processors"),
    ("CPU By Brand", "Dell CPU", "https://m4l.com/dell-cpu-processors"),
    ("CPU By Brand", "Fujitsu CPU", "https://m4l.com/fujitsu-cpu-processors"),
    ("CPU By Brand", "HP CPU", "https://m4l.com/hp-cpu-processors"),
    ("CPU By Brand", "IBM CPU", "https://m4l.com/ibm-cpu-processors"),
    ("CPU By Brand", "Intel CPU", "https://m4l.com/intel-cpu-processors"),
    ("CPU By Brand", "Lenovo CPU", "https://m4l.com/lenovo-cpu-processors"),
    ("CPU By Brand", "Sun CPU", "https://m4l.com/sun-cpu-processors"),
    ("CPU By Brand", "Toshiba CPU", "https://m4l.com/toshiba-cpu-processors"),
    ("Server CPU", "Intel Xeon Scalable CPU", "Intel Xeon Platinum", "https://m4l.com/intel-xeon-platinum-server-cpu-processors"),
    ("Server CPU", "Intel Xeon Scalable CPU", "Intel Xeon Gold", "https://m4l.com/intel-xeon-gold-server-cpu-processors"),
    ("Server CPU", "Intel Xeon Scalable CPU", "Intel Xeon Silver", "https://m4l.com/intel-xeon-silver-server-cpu-processors"),
    ("Server CPU", "Intel Xeon Scalable CPU", "Intel Xeon Bronze", "https://m4l.com/intel-xeon-bronze-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E7 Family", "Xeon E7 Family - v4", "https://m4l.com/intel-e7-v4-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E7 Family", "Xeon E7 Family - v3", "https://m4l.com/intel-e7-v3-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E7 Family", "Xeon E7 Family - v2", "https://m4l.com/intel-e7-v2-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E7 Family", "Xeon E7 Family", "https://m4l.com/intel-e7-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E5 Family", "Xeon E5 Family - v4", "https://m4l.com/intel-e5-v4-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E5 Family", "Xeon E5 Family - v3", "https://m4l.com/intel-e5-v3-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E5 Family", "Xeon E5 Family - v2", "https://m4l.com/intel-e5-v2-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E5 Family", "Xeon E5 Family", "https://m4l.com/intel-e5-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family - v6", "https://m4l.com/intel-e3-v6-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family - v5", "https://m4l.com/intel-e3-v5-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family - v4", "https://m4l.com/intel-e3-v4-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family - v3", "https://m4l.com/intel-e3-v3-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family - v2", "https://m4l.com/intel-e3-v2-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E3 Family", "https://m4l.com/intel-e3-xeon-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon E Family", "https://m4l.com/intel-xeon-e-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon D Family", "https://m4l.com/intel-xeon-d-server-cpu-processors"),
    ("Server CPU", "Intel Xeon E3 Family", "Xeon W Family", "https://m4l.com/intel-xeon-w-server-cpu-processors"),
    ("Desktop CPU", "Intel Core X-series CPU", "Intel Core i9 X-series", "https://m4l.com/intel-core-i9-x-series-desktop-cpu-processors"),
    ("Desktop CPU", "Intel Core X-series CPU", "Intel Core i9 Extreme Edition", "https://m4l.com/intel-core-i9-x-series-extreme-edition-desktop-cpu-processors"),
    ("Desktop CPU", "Intel Core X-series CPU", "Intel Core i7 X-series", "https://m4l.com/intel-core-i7-x-series-desktop-cpu-processors"),
    ("Desktop CPU", "Intel Core X-series CPU", "Intel Core i7 Extreme Edition", "https://m4l.com/intel-core-i7-x-series-extreme-edition-desktop-cpu-processors"),
    ("Desktop CPU", "Intel Core X-series CPU", "Intel Core i5 X-series", "https://m4l.com/intel-core-i5-x-series-desktop-cpu-processors"),
    ("Desktop CPU", "8th Generation Intel", "Intel Core i7 Gen8", "https://m4l.com/intel-8th-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "8th Generation Intel", "Intel Core i5 Gen8", "https://m4l.com/intel-8th-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "8th Generation Intel", "Intel Core i3 Gen8", "https://m4l.com/intel-8th-generation-core-i3-desktop-cpu-processors"),
    ("Desktop CPU", "7th Generation Intel", "Intel Core i7 Gen7", "https://m4l.com/intel-7th-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "7th Generation Intel", "Intel Core i5 Gen7", "https://m4l.com/intel-7th-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "7th Generation Intel", "Intel Core i3 Gen7", "https://m4l.com/intel-7th-generation-core-i3-desktop-cpu-processors"),
    ("Desktop CPU", "6th Generation Intel", "Intel Core i7 Gen6", "https://m4l.com/intel-6th-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "6th Generation Intel", "Intel Core i5 Gen6", "https://m4l.com/intel-6th-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "6th Generation Intel", "Intel Core i3 Gen6", "https://m4l.com/intel-6th-generation-core-i3-desktop-cpu-processors"),
    ("Desktop CPU", "5th Generation Intel", "Intel Core i7 Gen5", "https://m4l.com/intel-5th-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "5th Generation Intel", "Intel Core i5 Gen5", "https://m4l.com/intel-5th-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "4th Generation Intel", "Intel Core i7 Gen4", "https://m4l.com/intel-4th-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "4th Generation Intel", "Intel Core i5 Gen4", "https://m4l.com/intel-4th-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "4th Generation Intel", "Intel Core i3 Gen4", "https://m4l.com/intel-4th-generation-core-i3-desktop-cpu-processors"),
    ("Desktop CPU", "3rd Generation Intel", "Intel Core i7 Gen3", "https://m4l.com/intel-3rd-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "3rd Generation Intel", "Intel Core i5 Gen3", "https://m4l.com/intel-3rd-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "3rd Generation Intel", "Intel Core i3 Gen3", "https://m4l.com/intel-3rd-generation-core-i3-desktop-cpu-processors"),
    ("Desktop CPU", "2nd Generation Intel", "Intel Core i7 Gen2", "https://m4l.com/intel-2nd-generation-core-i7-desktop-cpu-processors"),
    ("Desktop CPU", "2nd Generation Intel", "Intel Core i5 Gen2", "https://m4l.com/intel-2nd-generation-core-i5-desktop-cpu-processors"),
    ("Desktop CPU", "Intel pentium", "Intel Pentium", "https://m4l.com/intel-pentium-desktop-cpu-processors"),
    ("Desktop CPU", "Intel celeron", "Intel Celeron", "https://m4l.com/intel-celeron-desktop-cpu-processors"),
    ("Mobile CPU", "Intel Core X-series Mobile", "i7 X-Series Extreme Mobile", "https://m4l.com/intel-core-i7-x-series-extreme-edition-mobile-cpu-processors"),
    ("Mobile CPU", "8th Generation Intel", "Intel Core i7 Gen8 Mobile", "https://m4l.com/intel-8th-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "8th Generation Intel", "Intel Core i5 Gen8 Mobile", "https://m4l.com/intel-8th-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "8th Generation Intel", "Intel Core i3 Gen8 Mobile", "https://m4l.com/intel-8th-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "7th Generation Intel", "Intel Core i7 Gen7 Mobile", "https://m4l.com/intel-7th-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "7th Generation Intel", "Intel Core i5 Gen7 Mobile", "https://m4l.com/intel-7th-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "7th Generation Intel", "Intel Core i3 Gen7 Mobile", "https://m4l.com/intel-7th-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "7th Generation Intel", "Intel Core M Gen7", "https://m4l.com/intel-7th-generation-core-m-mobile-cpu-processors"),
    ("Mobile CPU", "6th Generation Intel", "Intel Core i7 Gen6 Mobile", "https://m4l.com/intel-6th-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "6th Generation Intel", "Intel Core i5 Gen6 Mobile", "https://m4l.com/intel-6th-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "6th Generation Intel", "Intel Core i3 Gen6 Mobile", "https://m4l.com/intel-6th-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "6th Generation Intel", "Intel Core M Gen6", "https://m4l.com/intel-6th-generation-core-m-mobile-cpu-processors"),
    ("Mobile CPU", "5th Generation Intel", "Intel Core i7 Gen5 Mobile", "https://m4l.com/intel-5th-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "5th Generation Intel", "Intel Core i5 Gen5 Mobile", "https://m4l.com/intel-5th-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "5th Generation Intel", "Intel Core i3 Gen5 Mobile", "https://m4l.com/intel-5th-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "5th Generation Intel", "Intel Core M Gen5", "https://m4l.com/intel-5th-generation-core-m-mobile-cpu-processors"),
    ("Mobile CPU", "4th Generation Intel", "Intel Core i7 Gen4 Mobile", "https://m4l.com/intel-4th-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "4th Generation Intel", "Intel Core i5 Gen4 Mobile", "https://m4l.com/intel-4th-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "4th Generation Intel", "Intel Core i3 Gen4 Mobile", "https://m4l.com/intel-4th-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen3 Mobile", "Intel Core i7 Gen3 Mobile", "https://m4l.com/intel-3rd-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen3 Mobile", "Intel Core i5 Gen3 Mobile", "https://m4l.com/intel-3rd-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen3 Mobile", "Intel Core i3 Gen3 Mobile", "https://m4l.com/intel-3rd-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Core i7 Gen2 Mobile", "https://m4l.com/intel-2nd-generation-core-i7-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Core i5 Gen2 Mobile", "https://m4l.com/intel-2nd-generation-core-i5-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Core i3 Gen2 Mobile", "https://m4l.com/intel-2nd-generation-core-i3-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Pentium Mobile", "https://m4l.com/intel-pentium-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Celeron Mobile", "https://m4l.com/intel-celeron-mobile-cpu-processors"),
    ("Mobile CPU", "Intel Core i7 Gen2 Mobile", "Intel Atom Mobile","https://m4l.com/intel-atom-mobile-cpu-processors")
)


def init_log():
    """Initialize progress log file"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "status", "category", "brand", "model", "url", "message"])

def log_progress(status, category, brand, model, url, message=""):
    """Log progress to CSV"""
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

def get_last_position(target_url):
    """Get last processed page for a given URL"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            relevant = [row for row in reader if row["url"] == target_url]
            
            if any(row["status"] == "completed" for row in relevant):
                return "completed"
                
            # Get last processed page
            processed = [row for row in relevant if row["status"] in ("processing", "error")]
            if processed:
                return processed[-1]["url"]
    except FileNotFoundError:
        pass
    return None

def write_to_csv(link, data):
    """Write product data to category CSV"""
    try:
        with open("m4l/processors/processor_links", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    except Exception as e:
        print(f"CSV write error: {str(e)}")
        raise

def process_link(link):
    """Process a single CPU link with resume capability"""
    base_url = link[-1]
    last_state = get_last_position(base_url)
    
    if last_state == "completed":
        print(f"Skipping already completed: {base_url}")
        return

    driver = Driver(uc=True, headless=False)
    current_url = base_url + "?pg=1&sort=popularity&sz=40" if last_state is None else last_state

    try:
        while True:
            # Log page processing start
            log_progress("processing", *link[:-1], current_url, "Page processing started")
            
            print(f"Processing: {current_url}")
            driver.uc_open_with_reconnect(current_url)
            driver.uc_gui_click_captcha()

            # Scroll to load all products
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Parse and extract products
            soup = BeautifulSoup(driver.page_source, "html.parser")
            products = soup.select("li.m4l-grid-view div.m4l-item-title a")
            
            product_data = []
            for product in products:
                product_url = product["href"]
                if product_url.startswith("/"):
                    product_url = f"https://www.m4l.com{product_url}"
    
                # Create proper CSV rows based on link length
                if len(link) == 3:
                    row = [link[0], link[1], "", product_url]  # Empty model column
                elif len(link) == 4:
                    row = [link[0], link[1], link[2], product_url]

                product_data.append(row)
            
            write_to_csv(link, product_data)

            # Handle pagination
            try:
                arrows = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li.arrow")
                next_arrow = arrows[-1] if arrows else None
                
                if next_arrow and "unavailable" not in next_arrow.get_attribute("class"):
                    next_url = next_arrow.find_element(By.TAG_NAME, "a").get_attribute("href")
                    current_url = next_url
                else:
                    log_progress("completed", *link[:-1], base_url, "All pages processed")
                    print(f"Completed: {base_url}")
                    break

            except Exception as e:
                log_progress("error", *link[:-1], current_url, f"Pagination error: {str(e)}")
                print(f"Pagination error: {str(e)}")
                break

    except Exception as e:
        log_progress("error", *link[:-1], current_url, f"Processing error: {str(e)}")
        print(f"Critical error processing {base_url}: {str(e)}")
    finally:
        driver.quit()

def main():
    init_log()
    
    for link in CPU_LINKS:
        try:
            process_link(link)
        except Exception as e:
            print(f"Error processing link {link}: {str(e)}")
            continue

if __name__ == "__main__":
    main()