# 📰 El País 

This project scrapes opinion articles from [El País](https://elpais.com/), translates the article titles from **Spanish to English** using a translation API, and saves the output into `.txt` files.

Supports **cross-browser and cross-device testing** using **BrowserStack**.

---

## 🚀 Features

- ✅ Scrapes top 5 articles from the **"Opinión"** section
- 🌐 Translates Spanish titles to English using **Rapid Translate Multi Traduction API**
- 💾 Saves results as timestamped `.txt` files in the `output/` folder
- 📱🖥️ Runs tests in **parallel** on multiple browsers/devices via **BrowserStack**
- 🔐 Stores API keys and credentials securely using `.env`

---

## 🧱 Project Structure

| File | Description |
|------|-------------|
| `main.py` | Run scraper locally using Chrome |
| `runner.py` | Runs scraper in parallel on BrowserStack |
| `scraper.py` | Contains the scraping logic using Selenium |
| `translator.py` | Calls the translation API |
| `utils.py` | Helper functions (e.g., save output) |
| `.env` | API keys and credentials (not checked into Git) |
| `output/` | Folder where result `.txt` files are stored |

---

## ⚙️ Setup Instructions

  1. Clone the repo
     
    git clone https://github.com/your-username/elpais-scraper.git
    cd elpais-scraper
  
  2. Create a virtual environment
     
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
  
  3. Install dependencies
     
    pip install -r requirements.txt
  
  4.Add a .env file
  
    RAPID_API_KEY=your_rapidapi_key
    BROWSERSTACK_USERNAME=your_username
    BROWSERSTACK_ACCESS_KEY=your_access_key

▶️ Run Locally

    python main.py

This will launch Chrome, scrape 5 opinion articles, translate the titles, and save the result.

☁️ Run on BrowserStack (Parallel Execution)

    python runner.py
    
   This will run the scraper in 5 parallel threads on:

    -Windows 10 (Chrome)
    -Windows 11 (Chrome)
    -Windows 11 (Firefox)
    -macOS (Safari)
    -iPhone 14


BrowserStack session names and test statuses are reported automatically.

📂 Output
    The results are saved as .txt files in the output/ folder:
    output/
       
        ├── articles_desktop_Chrome_20250712_120000.txt
        ├── articles_iPhone_14_20250712_120001.txt
    ...
    
Each file includes:
    
    Spanish title
    Translated title (English)
    Article preview
    Cover image (if available)

Author:
    
    Hritik Gupta
