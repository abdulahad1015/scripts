from bs4 import BeautifulSoup
import time , requests,csv


# def read_links_from_file(filename="memory_links.txt"):
#     with open(filename, "r", encoding="utf-8") as file:
#         links = [line.strip() for line in file if line.strip()]  # Strip whitespace and ignore empty lines
#     return links
start = time.time()

def append_to_csv(data, filename="ebay/ebay_scraped.csv"):
    with open(filename, "a",newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)
        

category = sub_category = sub_sub_category = part_no = title = manufacturer = image = price = description = condition = product_type = None
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
# }
urls = ["https://www.ebay.com/itm/335620589902?mkcid=16&mkevt=1&mkrid=711-127632-2357-0&ssspo=jEREqci3RUe&sssrc=2047675&ssuid=&widget_ver=artemis&media=COPY",
        "https://www.ebay.com/itm/403184979313",
        "https://www.ebay.com/itm/365206745206?_trkparms=amclksrc%3DITM%26aid%3D1110013%26algo%3DHOMESPLICE.SIMRXI%26ao%3D1%26asc%3D279998%26meid%3D5786b8661c454f1b885cde0337bab958%26pid%3D102015%26rk%3D10%26rkt%3D25%26itm%3D365206745206%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DSimRXIHPNativeV3WithPreranker%26brand%3DDell&_trksid=p2332490.c102015.m3021&itmprp=cksum%3A3652067452065786b8661c454f1b885cde0337bab958%7Cenc%3AAQAJAAABACvGsIvGnI%252ByOHvfXLh5h7pw5T%252FuKX4Osb%252F2kabYqRkIXrosJsI47ytvZhZkXXOHS2wqFkjJJUTD8isuYUZbv2q23TCkbYhzJp5oHqj95W1cpuixk%252BXREBLmG%252B2vqIDuC4hBYAQ86fps%252Fz56MCQn2gGDz1uklZwqRtX30OMd%252Bj7ji4wAwebrsNOZy%252FViXkAm%252BGtRETqzTg%252FvAoyKN%252B3mR8iUDrbD3APxJPd1nt8aJTbdU1bElDraP7nt0fmlhhqpT99sxYlTa90r6g%252FlB4Y7FvyaTH%252FlcNG5wpucUexF4a6XPVmWsNz3l0UoR851zQZGeLeslWWHt4U3GmUatiC9yq0%253D%7Campid%3APL_CLK%7Cclp%3A2332490&itmmeta=01JKDTSRRY1GCGP0N6G8C355J3",
        "https://www.ebay.com/itm/396169469126?_trkparms=amclksrc%3DITM%26aid%3D1110013%26algo%3DHOMESPLICE.SIMRXI%26ao%3D1%26asc%3D279998%26meid%3D5786b8661c454f1b885cde0337bab958%26pid%3D102015%26rk%3D19%26rkt%3D25%26itm%3D396169469126%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DSimRXIHPNativeV3WithPreranker%26brand%3DSony&_trksid=p2332490.c102015.m3021&itmprp=cksum%3A3961694691265786b8661c454f1b885cde0337bab958%7Cenc%3AAQAJAAABACvGsIvGnI%252ByOHvfXLh5h7pw5T%252FuKX4Osb%252F2kabYqRkIXrosJsI47ytvZhZkXXOHS1DHQeV6ZAccBgVUQQR%252BfiECAuBr5hA%252B2xKuCF0Dba6dRZ%252Ffo77kA3K3kMQX7PLbjPrcmPKX0TCkrhAXfWfkrB6O5viLCoo%252FZn1OFVqTZpt%252BT0PuanPOkXKIFGxKs%252BGCMAnLcwYk2Ao4hjKDiytQnHwFHmZPMVG1HiwZfxJg0u2ENWr90cwGs25yyyIgwXaSTNA4fTaPgBTYg9HKzDBiLMLbeKP1QNVRAyq2ENqDKnuGVG9ZMzQcfP%252FQxsYzU1La55PtI3%252B1ZjDloIqeSSKeNoE%253D%7Campid%3APL_CLK%7Cclp%3A2332490&itmmeta=01JKDTSRS1X66WVJ33WCF9XAVZ",
        "https://www.ebay.com/itm/356479987691?_trkparms=amclksrc%3DITM%26aid%3D1110013%26algo%3DHOMESPLICE.SIMRXI%26ao%3D1%26asc%3D279998%26meid%3D5786b8661c454f1b885cde0337bab958%26pid%3D102015%26rk%3D23%26rkt%3D25%26itm%3D356479987691%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DSimRXIHPNativeV3WithPreranker%26brand%3DSony&_trksid=p2332490.c102015.m3021&itmprp=cksum%3A3564799876915786b8661c454f1b885cde0337bab958%7Cenc%3AAQAJAAABACvGsIvGnI%252ByOHvfXLh5h7pw5T%252FuKX4Osb%252F2kabYqRkIXrosJsI47ytvZhZkXXOHS9TX5RMglnSVEo9Z5RqBG3rv9NFaujndVQEgmMyU2b%252Fu9YZjNo1jgvCTut9TQV20TGK9eIlzFL8bo1sfPkKXMT8zYVsU1aCgEjQINkaTjpJGDjvTjKUN6DNEYokRvTePFXAWav6PvZ5HuhxCpIGuXfritfmy5O6m71An9EiXY8DJgL%252Bk8e4SQXEvM5ouRV0uOSxQxMuWHvg9tDGpfvD2NaJcr3LowP5LP32gDJGOoBC%252FjD4gl5MfHRbxkwElNnFiZWY8RIX%252B%252F08XT4fq1M8Z8Og%253D%7Campid%3APL_CLK%7Cclp%3A2332490&itmmeta=01JKDTSRS49TM0CB53834629DC",
        "https://www.ebay.com/itm/393476013073?_trksid=p2332490.c102015.m3021&itmprp=cksum%3A3934760130735786b8661c454f1b885cde0337bab958%7Cenc%3AAQAJAAABACvGsIvGnI%252ByOHvfXLh5h7pw5T%252FuKX4Osb%252F2kabYqRkIXrosJsI47ytvZhZkXXOHS9TQ",

        ]

for url in urls:
    try:
        response = requests.get(f"{url}")
        new_soup = BeautifulSoup(response.content, "html.parser")

        if new_soup.find("p", class_="error-header-v2__title"):
            print(f"Error: {new_soup.find('p', class_='error-header-v2__title').get_text()}")
            row = ("NA","Item not found","NA","NA",url,)
            append_to_csv(row)
            continue

        title = new_soup.find("h1") if new_soup.find("h1") else "NA"
        title = title.find("span").get_text() if title.find("span") else "NA"
       
        stock= new_soup.find("div", class_="x-quantity__availability").find("span").get_text() if new_soup.find("div", class_="x-quantity__availability") else "NA"
        
        price = new_soup.find("div", class_="x-price-primary").find("span").get_text(strip=True) if new_soup.find("div", class_="x-price-primary") else "NA"
        shipping_span = new_soup.find("div", class_="ux-labels-values col-12 ux-labels-values--shipping") if new_soup.find("div", class_="ux-labels-values col-12 ux-labels-values--shipping") else "NA"
        shipping_span = new_soup.find("div", class_= "ux-labels-values__values col-9").find_all("span")
        shipping = (shipping_span[0].get_text())

        row = (title,stock,price,shipping,url,)
        append_to_csv(row)
        print(row)

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(20)
print(f"Time taken: {time.time()-start}s")
