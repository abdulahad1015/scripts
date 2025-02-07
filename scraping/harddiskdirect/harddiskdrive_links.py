import csv
from seleniumbase import Driver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By

# CSV file setup
csv_file = 'memory_links.txt'

def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Initialize the undetected driver with SeleniumBase
driver = Driver(uc=True)  # Enable undetected-chromedriver mode

# Target URL
url = "https://harddiskdirect.com/categories/memory.html"

# Open the page and handle potential CAPTCHA
try:
    # Attempt to open the URL with reconnect logic
    driver.uc_open_with_reconnect(url)
    driver.uc_gui_click_captcha()  # Attempt to handle CAPTCHA interactively

    while True:
        # Scroll to the bottom to load all products
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Allow time for new content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parse the current page's source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all("div", class_="product-single-card")

        # Extract data for each producrt
        data = []
        for product in products:
            link_tag = product.find("a", href=True)
            product_url = link_tag['href'] if link_tag else "N/A"
            data.append([product_url])
            print(product_url)
        # Write the extracted data to the CSV
        write_to_csv(data)

        # Check if the next button is available and clickable
        try:
            # Wait for the "Next" button to become visible
            next_button = driver.find_element(By.XPATH, "//img[contains(@alt, 'right') and contains(@src, '/assets/svg/arrow-right.svg')]")
            # Scroll into view and click the button
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
        except Exception as e:
            print("No more pages or next button not found.")
            print(f"Error details: {e}")
            break  # Exit the loop if there are no more pages

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Quit the driver
    driver.quit()
