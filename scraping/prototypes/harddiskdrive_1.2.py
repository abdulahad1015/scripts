import csv
from seleniumbase import Driver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

csv_file = 'memory_data.csv'


category = sub_category = sub_sub_category = part_no = title = manufacturer = image = price = description = condition = product_type = None

def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header only if the file is empty
            writer.writerow(['Title', 'Price', 'Part Number', 'Image Source'])
        writer.writerows(data)

driver = Driver(uc=True)  # Enable undetected-chromedriver mode

url = "https://harddiskdirect.com/categories/storage-devices/hard-drives.html"

try:
    driver.uc_open_with_reconnect(url)
    driver.uc_gui_click_captcha()  # Attempt to handle CAPTCHA interactively

    while True:
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all("div", class_="product-single-card")

        data = []
        for product in products:
            img_tag = product.find("img", recursive=True)
            img_src = img_tag.get("src")
            # print(img_src)
            if img_tag:
                try:
                    img_element = driver.find_element(By.XPATH, f"//img[@src='{img_src}']")
                    actions = ActionChains(driver)
                    actions.click(img_element).perform()
                    time.sleep(5)
#//---------------------Extracting Data----------------------------------------//
                    new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    a_tags = new_soup.select("ul.custom-bread-crumb a")
                    a_tags.pop(0)
                    category_names=[a.get_text() for a in a_tags]
                    print(category_names)

#//--------------------------END-----------------------------------------------//                   
                    driver.back()
                    time.sleep(5)
                except Exception as e:
                    print(f"Error opening image in new tab: {e}")

        # write_to_csv(data)

        # try:
        #     next_button = driver.find_element(By.XPATH, "//img[contains(@alt, 'right') and contains(@src, '/assets/svg/arrow-right.svg')]")
        #     driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        #     driver.execute_script("arguments[0].click();", next_button)
        #     time.sleep(7)  # Allow time for the next page to load
        # except Exception as e:
        #     print("No more pages or next button not found.")
        #     print(f"Error details: {e}")
        #     break  # Exit the loop if there are no more pages

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()