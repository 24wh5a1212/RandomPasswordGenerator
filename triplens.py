from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Make sure chromedriver is in PATH)
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")
    time.sleep(2)

    # Find the search bar and enter a query
    search_box = driver.find_element("name", "q")
    search_box.send_keys("famous landmarks")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Click on the first search result
    first_result = driver.find_element("xpath", "(//h3)[1]")
    first_result.click()
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
