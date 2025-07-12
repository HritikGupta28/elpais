import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from translator import translate_texts
from datetime import datetime, timezone


def scrape_articles(driver):
    BASE_URL = "https://elpais.com"
    ARTICLE_LIMIT = 5

    # Navigate to homepage
    driver.get(BASE_URL)
    time.sleep(2)

    # Accept cookies
    try:
        cookie_btn = driver.find_element(By.ID, "didomi-notice-agree-button")
        cookie_btn.click()
        print("✅ Cookie banner accepted.")
    except:
        print("ℹ️ Cookie banner not found.")



    # Navigate to Opinion section
    try:
        opinion_button = driver.find_element(By.XPATH, '//*[@id="csw"]/div[1]/nav/div/a[2]')
        opinion_button.click()
        opinion_clicked = True
        print("✅ 'Opinión' button clicked.")
        time.sleep(2)
    except Exception as e:
        print(f"❌ 'Opinión' button not found or not clickable: {e}")
        opinion_clicked = False

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.select("article")[:ARTICLE_LIMIT]

    scraped_data = []
    titles_es = []

    for article in articles:
        h2 = article.find("h2")
        a_tag = article.find("a")
        if not h2 or not a_tag:
            continue

        title_es = h2.get_text(strip=True)
        href = a_tag.get("href")
        url = urljoin(BASE_URL, href) if href else None

        if not url:
            continue

        titles_es.append(title_es)

        scraped_data.append({
            "title_es": title_es,
            "url": url
        })

    if not scraped_data:
        print("❌ No articles found to scrape.")
        return []

    print("🔠 Titles to translate:", titles_es)
    translated_titles = translate_texts(titles_es)
    print("🟢 Translations:", translated_titles)

    os.makedirs("images", exist_ok=True)

    for i, article in enumerate(scraped_data):
        driver.get(article["url"])
        time.sleep(2)

        detail_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Get content
        paragraphs = detail_soup.select("p")
        content = "\n".join(p.get_text() for p in paragraphs[:5]) if paragraphs else "[No content]"

        # Get cover image
        img_tag = detail_soup.select_one("figure img[src^='https']")
        img_url = urljoin(article["url"], img_tag["src"]) if img_tag else None

        # Save image
        safe_title = re.sub(r"[^\w\s-]", "", article["title_es"]).strip().replace(" ", "_")
        img_path = "[No image found]"

        if img_url and img_url.startswith("http"):
            img_path = os.path.join("images", f"{safe_title}.jpg")
            try:
                img_data = requests.get(img_url).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
            except Exception as e:
                print(f"⚠️ Failed to download image: {e}")
                img_path = "[Image download failed]"

        article.update({
            "title_en": translated_titles[i] if i < len(translated_titles) else "[Translation failed]",
            "content": content,
            "img": img_path
        })

        print(f"✅ Scraped article {i+1}: {article['title_es']}")

    return scraped_data
