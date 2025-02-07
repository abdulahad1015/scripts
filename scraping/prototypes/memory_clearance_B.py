from seleniumbase import Driver

driver = Driver(uc=True)
url = "https://harddiskdirect.com/categories/memory/dell-memory.html"
driver.uc_open_with_reconnect(url, 4)
driver.uc_gui_click_captcha()


driver.quit()