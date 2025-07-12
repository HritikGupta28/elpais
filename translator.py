import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("RAPID_API_KEY")

# Set API constants
API_URL = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com"
}

def translate_texts(texts, source="es", target="en"):
    """
    Translates a list of texts from source to target language using Rapid Translate API.

    :param texts: List of strings to translate.
    :param source: Source language code (default "es").
    :param target: Target language code (default "en").
    :return: List of translated texts or placeholder on failure.
    """
    payload = {
        "from": source,
        "to": target,
        "e": "",
        "q": texts
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data
        else:
            return ["[Translation failed]"] * len(texts)

    except Exception as e:
        print("❌ Translation API error:", e)
        return ["[Translation failed]"] * len(texts)
