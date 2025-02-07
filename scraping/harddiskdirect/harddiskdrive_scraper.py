from selenium import webdriver
from bs4 import BeautifulSoup
import json , time
from pprint import pprint


def read_links_from_file(filename="memory_links.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        links = [line.strip() for line in file if line.strip()]  # Strip whitespace and ignore empty lines
    return links

def append_to_json(data, filename="memory.json"):
    with open(filename, "a", encoding="utf-8") as outfile:
        outfile.write(json.dumps(data, indent=4) + ",\n")

category = sub_category = sub_sub_category = part_no = title = manufacturer = image = price = description = condition = product_type = None
links = read_links_from_file("memory_links.txt")
driver = webdriver.Chrome()
Products = {}
url = "https://harddiskdirect.com"

for link in links:
    try:
        driver.get(f"{url}{link}")
        new_soup = BeautifulSoup(driver.page_source, 'html.parser')

        a_tags = new_soup.select("ul.custom-bread-crumb a")
        if a_tags:
            a_tags.pop(0)
        else:
            raise ValueError("Breadcrumb navigation not found")

        category_names = [a.get_text() for a in a_tags]
        category = category_names[0] if len(category_names) > 0 else "NA"
        sub_category = category_names[1] if len(category_names) > 1 else "NA"
        sub_sub_category = category_names[2] if len(category_names) > 2 else "NA"

        title = new_soup.find("h1").get_text(strip=True) if new_soup.find("h1") else "NA"
        description = new_soup.find("div", class_="desc").get_text(strip=True) if new_soup.find("div", class_="desc") else "NA"
        price = new_soup.find("p", class_="atc-price").get_text(strip=True) if new_soup.find("p", class_="atc-price") else "NA"
        image = new_soup.find("img", class_="slickImage").get("src") if new_soup.find("img", class_="slickImage") else "NA"
        condition = new_soup.find("span",class_="ps-2").get_text() if new_soup.find("span",class_="ps-2") else "NA"
        part = new_soup.find_all("p", class_="tablecolumn")
        manufacturer = part[0].get_text() if len(part) > 0 else "NA"
        part_no = part[1].get_text() if len(part) > 1 else "NA"

        Products = {
            "Part No":part_no,
            "Brand": manufacturer,
            "Category": category,
            "sub_category": sub_category,
            "sub_sub_category": sub_sub_category,
            "Title": title,
            "Description": description,
            "Condition":condition,
            "Price": price,
            "Image": image,
            "General Information": {},
            "Technical Information": {},
            "Miscellaneous": {}
        }

        tables = new_soup.find_all("div", class_="tablecustom")
        for table in tables:
            table_name = table.find("p", class_="headtable").get_text()
            rows = table.find_all("div", class_="tablerow")
            for row in rows:
                columns = row.find_all("div", class_="tablecolumn")
                if len(columns) == 2:
                    key = columns[0].find("span").get_text()
                    value = columns[1].find("span").get_text()
                    Products[table_name][key] = value

        append_to_json(Products)
        pprint(Products)

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(20)

driver.quit()
