from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome()

# Function to scroll the page and wait for images to load
def scroll_and_wait_for_images():
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'ng-lazyloaded')]"))
    )

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to allow new images to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit if we reach the end of the page
        last_height = new_height

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'ng-lazyloaded')]"))
        )

# Function to check if "Next" button is disabled
def is_next_button_disabled():
    try:
        # Locate the "Next" button and check if it's disabled
        next_button = driver.find_element(By.XPATH, "//li/button[contains(@class, 'simple-button')]")
        return 'disabled' in next_button.get_attribute("class")
    except:
        return True

# Start scraping and paginate
driver.get('https://www.memoryclearance.com/categories/memory/server-memory.html')

while True:
    # Scroll the page and wait for images to load
    scroll_and_wait_for_images()

    # Get the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product cards and extract details
    products = soup.find_all("div", class_="product-single-card")
    data = []
    
    for product in products:
        img_tag = product.find("img", recursive=True)
        img_src = img_tag.get("src") if img_tag else "N/A"
        title = product.find("h2", class_="p-title").get_text(strip=True) if product.find("h2", class_="p-title") else "N/A"
        price = product.find("span", class_="p-price").get_text(strip=True) if product.find("span", class_="p-price") else "N/A"
        card_div = product.find("div", class_="p-details")
        table = card_div.find("table", recursive=True) if card_div and card_div.find("table", recursive=True) else "N/A"
        
        data.append([title, price, table, img_src])
    
    # Print the data for checking
    for item in data:
        print(item)

    # Check if "Next" button is disabled
    if is_next_button_disabled():
        print("No more pages.")
        break  # Exit the loop if there are no more pages

    # Click the "Next" button to go to the next page    
    next_button = driver.find_element(By.XPATH, "//i[contains(@class, 'fa-angle-right')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    driver.execute_script("arguments[0].click();", next_button)
    # Wait for the page to load after clicking "Next"
    time.sleep(5)

# Close the driver after finishing
driver.quit()
