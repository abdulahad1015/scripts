import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

csv_file = 'memory_data.csv'

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

def is_next_button_disabled():
    try:
        next_button = driver.find_element(By.XPATH, "//li/button[contains(@class, 'simple-button')]")
        return 'disabled' in next_button.get_attribute("class")
    except:
        return True

def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Title', 'Price', 'Table', 'Image Source'])
        writer.writerows(data)

driver.get('https://www.memoryclearance.com/categories/memory/server-memory.html')

while True:
    scroll_and_wait_for_images()

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    products = soup.find_all("div", class_="product-single-card")
    data = []
    
    for product in products:
        img_tag = product.find("img", recursive=True)
        img_src = img_tag.get("src") if img_tag else "N/A"
        title = product.find("h2", class_="p-title").get_text(strip=True) if product.find("h2", class_="p-title") else "N/A"
        price = product.find("span", class_="p-price").get_text(strip=True) if product.find("span", class_="p-price") else "N/A"
        card_div = product.find("div", class_="p-details")
        table = card_div.find("table", recursive=True) if card_div and card_div.find("table", recursive=True) else "N/A"
        part_number = title.split(" ")
        data.append([title, price, part_number[1], img_src])

    write_to_csv(data)

    if is_next_button_disabled():
        print("No more pages.")
        break  

    next_button = driver.find_element(By.XPATH, "//i[contains(@class, 'fa-angle-right')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    driver.execute_script("arguments[0].click();", next_button)
    time.sleep(5)

driver.quit()
