import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.flipkart.com/")

try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='_2KpZ6l _2doB4z']"))
    )
    close_button.click()
except:
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("mobiles under 10000")
    search_box.send_keys(Keys.RETURN)
    print("Searched for mobiles under 10000.")
except:
    print("Error finding the search box.")

try:
    phone_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='CGtC98']"))
    )
except:
    print("Error finding phone links.")

for index, phone_link in enumerate(phone_links):
    try:
        phone_link.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[-1])
        try:
            driver.execute_script("window.scrollTo(0, 2000);")
            time.sleep(2)
        except:
            pass

        try:
            read_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "QqFHMw _4FgsLt"))
            )
            read_more_button.click()
            time.sleep(2)
        except:
            pass

        try:
            dimensions_block = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//td[text()='Weight']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", dimensions_block)
            time.sleep(2)
            weight_element = driver.find_element(By.XPATH, "//td[text()='Weight']/following-sibling::td//li")
            phone_weight = weight_element.text
            print(f"Phone {index + 1} Weight: {phone_weight}")

        except:
            print(f"Phone {index + 1} Weight: Not found")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except:
        pass

driver.quit()