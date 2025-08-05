import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Setup ChromeDriver 
options = Options()
options.add_argument("startmaximized")
driver_path = "chromedriver.exe"  

driver = webdriver.Chrome(service=Service(driver_path), options=options)
 
url = "https://www.reuters.com/"
driver.get(url)
time.sleep(5)

# load articles 
for _ in range(5): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
 
articles_data = []
articles = driver.find_elements(By.TAG_NAME, "article")

for article in articles:
    try:
        # URL and Title
        link_element = article.find_element(By.TAG_NAME, "a")
        url = link_element.get_attribute("href")
        title = link_element.text.strip()

        # Description
        try:
            desc = article.find_element(By.TAG_NAME, "p").text.strip()
        except NoSuchElementException:
            desc = "N/A"

        # Date 
        try:
            date = article.find_element(By.TAG_NAME, "time").get_attribute("datetime")
        except NoSuchElementException:
            date = "N/A"

        articles_data.append({
            "URL": url,
            "Title": title,
            "Description": desc,
            "Date": date
        })

    except Exception as e:
        print("Skipping one article due to error:", e)

# Store to CSV 
df = pd.DataFrame(articles_data)
df.to_csv("reuters_articles.csv", index=False)
print(f"\nScraped {len(df)} articles. Saved to 'reuters_articles.csv'.")

driver.quit()
