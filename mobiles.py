from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

driver = webdriver.Chrome()

driver.get("https://www.flipkart.com")


try:
    close_login_popup = driver.find_element(By.XPATH, "//button[@class='_2KpZ6l _2doB4z']")
    close_login_popup.click()
except:
    pass

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("mobile phones under 10000")
search_box.send_keys(Keys.RETURN)

phones_list = []

phones_scraped = 0
max_phones = 24 
page_number = 1
max_pages = 3  

while phones_scraped < max_phones and page_number <= max_pages:
    
    time.sleep(5)

    phones = driver.find_elements(By.XPATH, "//div[@class='_4rR01T']")
    prices = driver.find_elements(By.XPATH, "//div[@class='_30jeq3 _1_WHN1']")
    ratings = driver.find_elements(By.XPATH, "//div[@class='_3LWZlK']")
    specs = driver.find_elements(By.XPATH, "//ul[@class='_1xgFaf']")
    print(f"Number of phones found:{len(phones)}")
    print(f"Number of prices found:{len(prices)}")
    print(f"Number of ratings found:{len(ratings)}")
    print(f"Number of specs found:{len(specs)}")

    for phone, price, rating, spec in zip(phones, prices, ratings, specs):
        if phones_scraped >= max_phones:
            break

        details = spec.text.split("\n")
        ram = next((d for d in details if "RAM" in d), "N/A")
        battery = next((d for d in details if "Battery" in d), "N/A")

        phones_list.append({
            "Name": phone.text,
            "Rating": rating.text,
            "Price": price.text,
            "RAM": ram,
            "Battery": battery
        })
        phones_scraped += 1

    if phones_scraped >= max_phones:
        break

    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='_1LKTO3'][contains(text(), 'Next')]")
        next_button.click()
        page_number += 1
    except:
        break

driver.quit()
