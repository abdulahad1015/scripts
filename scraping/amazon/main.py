from bs4 import BeautifulSoup
import time , requests,csv, browser_cookie3
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

driver = Driver()
driver.maximize_window()
driver.get("https://www.amazon.com/dp/B0D7HPK91S")
time.sleep(50)
# def read_links_from_file(filename="memory_links.txt"):
#     with open(filename, "r", encoding="utf-8") as file:
#         links = [line.strip() for line in file if line.strip()]  # Strip whitespace and ignore empty lines
#     return links
start = time.time()

# def append_to_csv(data, filename="amazon/amazon_scraped.csv"): 
#     with open(filename, "a",newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(data)
        

# title = price = stock = shipping = product_type = None
# headers = {
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
# "Accept-Language": "en-US,en;q=0.9",
# "Referer": "https://www.amazon.com/",
# "Host": "www.amazon.com"




# }
# urls = ["https://www.amazon.com/HP-DeskJet-2755e-Wireless-Printer/dp/B08XYP6BJV/?_encoding=UTF8&pd_rd_w=s6Iff&content-id=amzn1.sym.f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_p=f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_r=T36N0DEBKDPT4MGRT5NV&pd_rd_wg=emnXV&pd_rd_r=8c5426ec-3654-41e3-8a06-8b0c2aa503ef&ref_=pd_hp_d_btf_crs_zg_bs_541966&th=1",
#         "https://www.amazon.com/dp/B0DGRR95HF",
        
        
#         ]

# for url in urls:
#     try:
#         response = requests.get(f"{url}")
#         new_soup = BeautifulSoup(response.content, "html.parser")
#         print(response.status_code) 
#         if new_soup.find("p", class_="error-header-v2__title"):
#             print(f"Error: {new_soup.find('p', class_='error-header-v2__title').get_text()}")
#             row = ("NA","Item not found","NA","NA",url,)
#             append_to_csv(row)
#             continue

#         title = new_soup.find("h1",id="title") if new_soup.find("h1",id="title") else "NA"
#         title = title.find("span").get_text() if title.find("span") else "NA"
       
#         # stock= new_soup.find("div", class_="x-quantity__availability").find("span").get_text() if new_soup.find("div", class_="x-quantity__availability") else "NA"
        
#         price = new_soup.find("span", class_="a-price-whole").get_text(strip=True) if new_soup.find("span", class_="a-price-whole") else "NA"
#         # shipping_span = new_soup.find("div", class_="ux-labels-values col-12 ux-labels-values--shipping") if new_soup.find("div", class_="ux-labels-values col-12 ux-labels-values--shipping") else "NA"
#         # shipping_span = new_soup.find("div", class_= "ux-labels-values__values col-9").find_all("span")
#         # shipping = (shipping_span[0].get_text())

#         row = (title,stock,price,shipping,url,)
#         append_to_csv(row)
#         print(row)

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         time.sleep(20)
# print(f"Time taken: {time.time()-start}s")
