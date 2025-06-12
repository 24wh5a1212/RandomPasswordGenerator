

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome()

driver.implicitly_wait(5)

driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#time.sleep(5)
#driver.execute_script("window.scrollTo(0,0);")

searchElement = driver.find_element(By.XPATH, value="//input[@type='search']")

searchElement.send_keys("ber")
print("testing text value", searchElement.text)
print("testing value attribute",searchElement.get_attribute("value"))
print("testing with innerText",searchElement.get_attribute("innerText"))

vegetables = driver.find_elements(by=By.XPATH,value="//div[@class='product']")
print(f"number of vegetables = {len(vegetables)}")
for veges in vegetables:
    veges.find_element(by=By.XPATH, value="div/button").click()

driver.find_element(by=By.CLASS_NAME, value="cart-icon").click()
driver.find_element(by=By.XPATH, value="//div[@class='action-block']/button").click()
time.sleep(5)
driver.find_element(by=By.CLASS_NAME, value="promoCode").send_keys("rahulshettyacademy1")
driver.find_element(by=By.CLASS_NAME,value="promoBtn").click()
#myelement = driver.find_element(by=By.CLASS_NAME,value="promoInfo")

myelement=WebDriverWait(driver,timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME,"promoInfo")))
if (myelement.text).__contains__("Invalid code"):
    print("Invalid Coupon")
else:
    print("valid coupon")

time.sleep(5)
driver.close()