import os
import json
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from scraper import scrape_articles
from translator import translate_texts
from browserstack_utils import mark_test_status

# Load environment variables
load_dotenv()
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Load platform capabilities
with open("platforms.json", "r") as f:
    capabilities_list = json.load(f)

def write_articles_to_text(articles, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, article in enumerate(articles, start=1):
            f.write(f"Article {i}\n")
            f.write(f"Original Title (ES): {article.get('title_es', '[Missing]')}\n")
            f.write(f"Translated Title (EN): {article.get('translated_title', '[Missing]')}\n")
            f.write(f"URL: {article.get('url', '[Missing]')}\n")
            f.write(f"Image: {article.get('img', '[Missing]')}\n")
            f.write(f"Content:\n{article.get('content', '[Missing]')}\n")
            f.write("-" * 60 + "\n")

def run_test(capabilities: dict, index: int):
    from selenium.webdriver.common.options import ArgOptions

    options = ArgOptions()
    for key, value in capabilities.items():
        options.set_capability(key, value)

    session_name = capabilities.get("bstack:options", {}).get("sessionName", f"El Pais Test #{index + 1}")
    build_name = capabilities.get("bstack:options", {}).get("buildName", "El Pais Build")

    driver: WebDriver = None

    try:
        driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )

        print(f"✅ BrowserStack session started: {session_name}")

        # Scrape articles
        articles = scrape_articles(driver)

        if not articles:
            raise Exception("No articles scraped.")

        # Translate titles
        titles = [article.get("title_en") or article.get("title_es") for article in articles]
        translated_titles = translate_texts(titles)
        for i, title in enumerate(translated_titles):
            articles[i]["translated_title"] = title

        # Save to .txt file
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        device_name = capabilities.get("bstack:options", {}).get("deviceName") or f"{capabilities.get('os', 'desktop')}_{capabilities.get('browserName')}"
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"articles_{device_name}_{timestamp}.txt".replace(" ", "_"))

        write_articles_to_text(articles, filename)
        print(f"✅ Articles saved to {filename}")

        mark_test_status(driver, "passed", "Scraping and translation successful.")

    except Exception as e:
        print(f"❌ Error in thread #{index + 1}: {e}")
        try:
            if driver:
                mark_test_status(driver, "failed", str(e))
        except Exception as mark_err:
            print(f"⚠️ Failed to mark status on BrowserStack: {mark_err}")

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    threads = []

    for i, capabilities in enumerate(capabilities_list):
        t = threading.Thread(target=run_test, args=(capabilities, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("✅ All BrowserStack tests completed.")
