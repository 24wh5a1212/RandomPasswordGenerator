from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
driver = webdriver.Chrome()
driver.get("https://www.flipkart.com/")
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search for Products, Brands and More']"))
)
search_box.send_keys("mobiles under 10000")
search_box.send_keys("\n")
time.sleep(1)
mobile_data = []
for page in range(1, 4):
    print(f"\nExtracting data from Page {page}...\n")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'CGtC98')]"))
    )
    mobile_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'KzDlHZ')]") 
    price_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'Nx9bqj _4b5DiR')]")  
    rating_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'XQDdHH')]") 
    phone_urls = [phone.get_attribute("href") for phone in driver.find_elements(By.XPATH, "//a[contains(@class, 'CGtC98')]")]
    for i in range(len(mobile_elements)):
        try:
            mobile_name = mobile_elements[i].text
            price = price_elements[i].text if i < len(price_elements) else "No Price"
            rating = rating_elements[i].text if i < len(rating_elements) else "No Rating"
            phone_url = phone_urls[i] if i < len(phone_urls) else "No URL"
            driver.execute_script(f"window.open('{phone_url}', '_blank');")
            driver.switch_to.window(driver.window_handles[1])  

            try:
                read_more_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Read More')]"))
                )
                read_more_button.click()
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//tr[td[contains(text(), 'Weight')]]/td"))
                )
            except:
                pass  
            try:
                weight_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//tr[td[contains(text(), 'Weight')]]/td[2]"))
                )
                weight = weight_element.text
            except:
                weight = "Not Found"
            mobile_data.append({"Mobile Name": mobile_name, "Price": price, "Rating": rating, "Weight": weight})
            print(f"Extracted: {mobile_name} - {price} - {rating} - {weight}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])  
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(@class, "_9QVEpD")][last()]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
    except:
        print("No more pages or error clicking next.")
        break
df = pd.DataFrame(mobile_data)
df.to_csv("flipkart_mobiles_data.csv", index=False)

driver.quit()
print("\nData extraction complete! Saved to flipkart_mobiles_data.csv")