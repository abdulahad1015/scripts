import csv
import time
from seleniumbase import Driver
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By  # Fix the missing import

# CSV file setup
csv_file = 'memory_data_with_details.csv'

def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header only if the file is empty
            writer.writerow(['Title', 'Price', 'Part Number', 'Image Source', 'Product Details'])
        writer.writerows(data)

# Function to fetch product details from listing
def fetch_product_details(url):
    try:
        # Make sure the URL is complete (prepend domain if it's a relative URL)
        full_url = f"https://harddiskdirect.com{url}" if not url.startswith("http") else url

        detail_driver = Driver(uc=True, headless=True)
        detail_driver.get(full_url)
        soup = BeautifulSoup(detail_driver.page_source, 'html.parser')

        # Extract product details from the page
        details = soup.find("div", class_="product-description")  # Adjust this selector if needed
        details_text = details.get_text(strip=True) if details else "N/A"

        detail_driver.quit()
        return details_text
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        return "N/A"

# Main function for scraping
def main():
    driver = Driver(uc=True)
    url = "https://harddiskdirect.com/categories/processors.html"
    try:
        driver.uc_open_with_reconnect(url)
        driver.uc_gui_click_captcha()  # Attempt to handle CAPTCHA interactively

        while True:
            # Scroll to load all products
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all("div", class_="product-single-card")

            # Collect product data
            data = []
            product_urls = []  # Store URLs of individual listings
            for product in products:
                img_tag = product.find("img", recursive=True)
                img_src = img_tag.get("src") if img_tag else "N/A"
                title = product.find("h2", class_="p-title").get_text(strip=True) if product.find("h2", class_="p-title") else "N/A"
                price = product.find("span", class_="p-price").get_text(strip=True) if product.find("span", "p-price") else "N/A"
                part_number = title.split(" ")[1] if len(title.split(" ")) > 1 else "N/A"
                
                # Extract the product page URL
                link_tag = product.find("a", href=True)
                product_url = link_tag['href'] if link_tag else "N/A"
                if product_url != "N/A":
                    product_urls.append(product_url)

                data.append([title, price, part_number, img_src, "Pending"])

            # Fetch product details in parallel
            with ThreadPoolExecutor(max_workers=5) as executor:
                product_details = list(executor.map(fetch_product_details, product_urls))

            # Merge details back into data
            for i, details in enumerate(product_details):
                data[i][-1] = details  # Replace "Pending" with actual details

            # Write the combined data to CSV
            write_to_csv(data)

            # Check for the next page
            try:
                next_button = driver.find_element(By.XPATH, "//img[contains(@alt, 'right') and contains(@src, '/assets/svg/arrow-right.svg')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(12)
            except Exception as e:
                print("No more pages or next button not found.")
                print(f"Error details: {e}")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Run the script
if __name__ == "__main__":
    main()
