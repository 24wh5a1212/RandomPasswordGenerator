import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver.get("https://www.flipkart.com/")

# Close the login popup
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='✕']"))
    )
    close_button.click()
except Exception as e:
    print("Popup not found, trying to send 'Esc' key.")
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Search for mobiles under 10000
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("mobiles under 10000")
    search_box.send_keys(Keys.RETURN)
except Exception as e:
    print("Error finding the search box:", e)

# Wait for the results to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'_1AtVbE')]"))
    )
    print("Page loaded successfully.")
except Exception as e:
    print("Error loading results:", e)

mobile_data = []

# Function to extract mobile data
def extract_data():
    try:
        mobile_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'KzDlHZ')]")
        price_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'Nx9bqj _4b5DiR')]")
        ram_rom_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'J+igdf')][1]")
        display_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'J+igdf')][2]")
        battery_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'J+igdf')][3]")
        processor_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'J+igdf')][4]")

        for i in range(min(len(mobile_elements), len(price_elements), len(ram_rom_elements), len(display_elements), len(battery_elements), len(processor_elements))):
            name = mobile_elements[i].text
            price = price_elements[i].text
            ram_rom = ram_rom_elements[i].text if len(ram_rom_elements) > i else "N/A"
            display = display_elements[i].text if len(display_elements) > i else "N/A"
            battery = battery_elements[i].text if len(battery_elements) > i else "N/A"
            processor = processor_elements[i].text if len(processor_elements) > i else "N/A"
            
            mobile_data.append({
                'name': name,
                'price': price,
                'ram_rom': ram_rom,
                'display': display,
                'battery': battery,
                'processor': processor
            })
    except Exception as e:
        print("Error extracting data:", e)

# Loop through first 5 pages
page_count = 1
while page_count <= 5:
    extract_data()
    
    # Try to find the "Next" button and click it
    if page_count < 5:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='_9QVEpD']//span[text()='Next']"))  # XPath for the "Next" button
            )
            next_button.click()
            time.sleep(2)  # Give some time for the next page to load
        except Exception as e:
            print("Reached the last page or error:", e)
            break

    page_count += 1  # Increment page count after loading the next page

# Save data to CSV
with open('flipkart_phones.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Name", "Price", "RAM/ROM", "Display", "Battery", "Processor"])
    
    for mobile in mobile_data:
        writer.writerow([mobile['name'], mobile['price'], mobile['ram_rom'], mobile['display'], mobile['battery'], mobile['processor']])

print("Data saved to flipkart_phones.csv successfully!")

driver.quit()