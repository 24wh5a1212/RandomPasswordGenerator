from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.mayfairhotels.com/")

driver.find_element(by=By.XPATH, value="//button[@class='resv resv_button book_button']").click()
sleep(3)

driver.find_element(by=By.XPATH, value="//span[@class='select2-selection__arrow']").click()
sleep(3)

#driver.find_element(by=By.XPATH, value="//input[@class='select2-search__field']").send_keys("Goa")
driver.find_element(by=By.XPATH, value="//li[text()='Goa']").click()
sleep(5)


hotelList = driver.find_elements(by=By.XPATH, value="//input[@class='btn btn-full-width']")
print(len(hotelList))
for index, hotel in enumerate(hotelList):
            if hotel.is_displayed():
                print(f"i am in on {index+1} {hotel.is_displayed()},{hotel.is_selected()}, {hotel.is_enabled()},{hotel.text}")
                hotel.click()
                break
            #print(f"i am in on {index+1} {hotel.is_displayed()},{hotel.is_selected()}, {hotel.is_enabled()},{hotel.text}")
            #hotel.click()
            #break
sleep(5)
driver.quit()
