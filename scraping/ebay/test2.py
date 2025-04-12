from selenium import webdriver

# Initialize WebDriver (Ensure you have the correct WebDriver for your browser)
driver = webdriver.Chrome()  

with open("ebay.csv" , "r") as file:
    urls = file.readlines()



for url in urls:
    url = url.split(",")[1]
    driver.get(url)
    final_url = driver.current_url  
    if url != final_url:
        print(f"Redirect detected! Final URL:{url} - {final_url}")
    else:
        print("No redirection detected.")

# Close the browser
driver.quit()
