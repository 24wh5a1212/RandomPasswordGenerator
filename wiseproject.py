from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import pandas as pd

# -------------------- Utility Functions --------------------

prev_prices = []

def clean_price(price_text):
    try:
        price_text = price_text.strip().replace("Rs.", "").replace(",", "").replace("*", "")

        # Handle Lakh range
        if "Lakh" in price_text:
            match = re.findall(r"[\d.]+", price_text)
            if match:
                value = float(match[0])  # Take only the lower price
            else:
                raise ValueError("No numeric value found")

        # Handle Crore
        elif "Cr" in price_text:
            match = re.findall(r"[\d.]+", price_text)
            if match:
                value = float(match[0]) * 100
            else:
                raise ValueError("No numeric value found")

        else:
            raise ValueError("Unknown format")

        prev_prices.append(value)
        return round(value, 1)

    except:
        # fallback to mean of previous prices
        if prev_prices:
            fallback = round(sum(prev_prices) / len(prev_prices), 1)
        else:
            fallback = 10.0
        prev_prices.append(fallback)
        return fallback

def get_float(text):
    try:
        return float(re.sub(r"[^\d.]", "", text.strip()))
    except:
        return None

def get_int(text):
    try:
        return int(re.sub(r"[^\d]", "", text.strip()))
    except:
        return None

# -------------------- Selenium Setup --------------------

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-notifications")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.cardekho.com/newcars")
time.sleep(5)

# -------------------- Click Search Button --------------------

try:
    search_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Search")]')
    search_btn.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"card card_new")]'))
    )
except:
    print("Search button not found or cards did not load in time.")

# -------------------- Scroll to Load All Cards --------------------

prev_count = 0
same_count_tries = 0
max_tries = 20

while same_count_tries < max_tries:
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)
    cards = driver.find_elements(By.XPATH, '//section[contains(@class,"card card_new")]')
    if len(cards) == prev_count:
        same_count_tries += 1
    else:
        same_count_tries = 0
        prev_count = len(cards)

print(f"Total cards found: {len(cards)}")

# -------------------- Extract Data --------------------

unique_names = set()
data = []

for card in cards:
    try:
        name = card.find_element(By.XPATH, './/h3/a').text.strip()
        if "electric" in name.lower() or name in unique_names:
            continue
    except:
        continue

    try:
        price_text = card.find_element(By.XPATH, './/div[@class="price"]/span').text.strip()
        price = clean_price(price_text)
    except:
        price = clean_price("")

    try:
        mileage = get_float(card.find_element(By.XPATH, './/div[contains(@class,"dotlist")]//span[@title="Mileage"]').text)
    except:
        mileage = None

    try:
        engine = get_float(card.find_element(By.XPATH, './/div[contains(@class,"dotlist")]//span[@title="Engine Displacement"]').text)
    except:
        engine = None

    try:
        seating = get_int(card.find_element(By.XPATH, './/div[contains(@class,"dotlist")]/span[last()]').text)
        if seating is not None and (seating < 2 or seating > 10):
            seating = None
    except:
        seating = None

    try:
        rating = get_float(card.find_element(By.XPATH, './/span[contains(@class,"ratingStarNew")]').text)
    except:
        rating = None

    try:
        review = get_int(card.find_element(By.XPATH, './/a[contains(@class,"bottomText")]').text)
    except:
        review = None

    data.append([name, price, rating, review, mileage, engine, seating])
    unique_names.add(name)

driver.quit()

# -------------------- Create DataFrame --------------------

df = pd.DataFrame(data, columns=["Name", "Price (Lakh)", "Rating", "Review Count", "Mileage (kmpl)", "Engine (cc)", "Seating"])

# -------------------- Clean Missing Values --------------------

for col in ["Price (Lakh)", "Rating", "Review Count", "Mileage (kmpl)", "Engine (cc)", "Seating"]:
    if col != "Seating":
        df[col] = df[col].astype(float)
        mean_val = round(df[col].mean(), 1)
        df[col].fillna(mean_val, inplace=True)
    else:
        mean_val = int(round(df["Seating"].mean()))
        df["Seating"].fillna(mean_val, inplace=True)

df["Seating"] = df["Seating"].astype(int)
df["Review Count"] = df["Review Count"].astype(int)

# -------------------- Popularity Score --------------------

raw_popularity = df["Rating"] * df["Review Count"]
min_pop, max_pop = raw_popularity.min(), raw_popularity.max()
df["Popularity"] = raw_popularity.apply(lambda x: round(1 + 9 * (x - min_pop) / (max_pop - min_pop), 1) if max_pop > min_pop else 5.0)

# -------------------- Final Cleanup --------------------

df.drop_duplicates(subset="Name", inplace=True)
df.to_csv("cardekho_outer_data_cleaned.csv", index=False)

# -------------------- Summary --------------------

print("✅ Cleaned data saved to cardekho_outer_data_cleaned.csv")
print(f"✅ Final car count: {len(df)}")