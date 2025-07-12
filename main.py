from selenium import webdriver
from scraper import scrape_articles
from utils import save_to_json

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        print("🚀 Scraping articles from El País...")
        articles = scrape_articles(driver)

        if not articles:
            print("❌ No articles scraped.")
            return

        save_to_json(articles)

        for i, article in enumerate(articles, start=1):
            print(f"\n📄 Article {i}:")
            print(f"🗞️ Title (ES): {article.get('title_es', '[Missing]')}")
            print(f"🌍 Title (EN): {article.get('title_en', '[Missing]')}")
            print(f"📝 Content (preview):\n{article.get('content', '[No content]')[:500]}")
            print(f"🖼️ Image: {article.get('img', '[No image]')}")

    finally:
        driver.quit()
        print("\n✅ Done. Browser closed.")

if __name__ == "__main__":
    main()
