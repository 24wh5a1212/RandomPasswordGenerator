import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 🔹 Configure Selenium WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔹 Get User Input
brand = input("\nEnter car brand (e.g., BMW, Toyota, Ford): ").strip().lower()
model = input("Enter car model (or leave blank for all models): ").strip().lower()

# 🔹 Construct URL for Scraping
base_url = "https://www.cars.com/shopping/results/"
search_url = f"{base_url}?makes[]={brand}&models[]={brand}-{model}" if model else f"{base_url}?makes[]={brand}"

print(f"\n🔍 Searching for cars at: {search_url}")
driver.get(search_url)
time.sleep(5)  # Allow page to load

# 🔹 Scrape Car Details
soup = BeautifulSoup(driver.page_source, "html.parser")
cars = soup.find_all("div", class_="vehicle-card")

if not cars:
    print("❌ No results found for the given brand/model.")
    driver.quit()
    exit()

# 🔹 Create CSV File
csv_filename = "cars.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Car Name", "Model", "Mileage", "Price", "Dealer Name"])  # Headers

    for car in cars:
        title = car.find("h2").text.strip() if car.find("h2") else "No title"
        extracted_model = title.split(" ", 1)[1] if len(title.split(" ", 1)) > 1 else "No model"
        price = car.find("span", class_="primary-price").text.strip() if car.find("span", class_="primary-price") else "No price"
        mileage = car.find("div", class_="mileage").text.strip() if car.find("div", class_="mileage") else "No mileage"
        dealer_name = car.find("div", class_="dealer-name").text.strip() if car.find("div", class_="dealer-name") else "No dealer"

        writer.writerow([title, extracted_model, mileage, price, dealer_name])

driver.quit()
print(f"\n✅ Data saved to {csv_filename} 🚗💨")

# 🔹 Load Dataset for Machine Learning
df = pd.read_csv(csv_filename)

# 🔹 Handle Missing Values
df.fillna(df.median(numeric_only=True), inplace=True)

# 🔹 Convert Categorical Features
df = pd.get_dummies(df, columns=['Model'], drop_first=True)

# 🔹 Define Features & Target
df["Popularity"] = np.random.choice([0, 1], size=len(df))  # Simulated Popularity
X = df.drop(columns=['Car Name', 'Dealer Name', 'Popularity'])
y = df["Popularity"]

# 🔹 Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 Evaluate Model
y_pred = model.predict(X_test)
print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred))

# 🔹 Predict Popularity of Scraped Car
new_car = X.iloc[0].values.reshape(1, -1)
prediction = model.predict(new_car)
print("\n🚗 Popularity Prediction:", "Popular" if prediction[0] == 1 else "Not Popular")
