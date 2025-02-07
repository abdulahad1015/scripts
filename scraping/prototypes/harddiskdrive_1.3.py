import csv
from selenium import webdriver 
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas

csv_file = 'memory_data.csv'

driver = webdriver.Chrome()  # Enable undetected-chromedriver mode
category = sub_category = sub_sub_category = part_no = title = manufacturer = image = price = description = condition = product_type = None

def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header only if the file is empty
            writer.writerow(['Title', 'Price', 'Part Number', 'Image Source'])
        writer.writerows(data)



links = ["/500n5-dell-intel-unboxed-processor.html"
# ,"/t3f05-dell-intel-unboxed-processor.html"
# ,"/0ftpg-dell-intel-unboxed-processor.html"
# ,"/p1n05-dell-intel-unboxed-processor.html"
# ,"/c4kvv-dell-intel-unboxed-processor.html"
# ,"/7whpg-dell-intel-unboxed-processor.html"
# ,"/0x373-dell-intel-unboxed-processor.html"
# ,"/0x377-dell-intel-unboxed-processor.html"
# ,"/0x384-dell-intel-unboxed-processor.html"
# ,"/124kr-dell-intel-unboxed-processor.html"
# ,"/139cw-dell-intel-unboxed-processor.html"
,"/14whp-dell-intel-unboxed-processor.html"]
url = f"https://harddiskdirect.com"
driver.get(f"https://harddiskdirect.com")

for link in links:
    try:
        driver.get(f"https://harddiskdirect.com{link}")
        
    #//---------------------Extracting Data----------------------------------------//
        new_soup = BeautifulSoup(driver.page_source, 'html.parser')
        a_tags = new_soup.select("ul.custom-bread-crumb a")
        a_tags.pop(0)
        category_names=[a.get_text() for a in a_tags]
        category=category_names[0]
        sub_category=category_names[1]
        sub_sub_category=category_names[2] if len(category_names)==3 else "NA"

        title=new_soup.find("h1").get_text(strip=True) if new_soup.find("h1") else "NA"
        description = new_soup.find("div",class_="desc").get_text(strip=True) if new_soup.find("div",class_="desc") else "NA"
        price = new_soup.find("p",class_="atc-price").get_text(strip=True) if new_soup.find("p",class_="atc-price") else "NA"
        image= new_soup.find("img",class_="slickImage").get("src") if new_soup.find("img",class_="slickImage").get("src") else "NA"
        rows = new_soup.find_all("div",class_="tablerow")

        data={}
        for row in rows:
            if row.find_all("div",class_="tablecolumn"):
                columns = row.find_all("div",class_="tablecolumn")  
                print((columns[0].find("span")).get_text(),(columns[1].find("span")).get_text())
            else:
                pass 
            # for column in columns:
            # data[column[0].get_text(strip=True)]=column[1].get_text(strip=True)
            
        
        
        # title = product.find("h2", class_="p-title").get_text(strip=True) if product.find("h2", class_="p-title") else "N/A"
        # print(f"Title:{title}\nCategory:{category_names}\n Description{description}\nPrice:{price}\nImage:{image}")
        # print(data)
    #//--------------------------END-----------------------------------------------//                   
               
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pass
driver.quit()