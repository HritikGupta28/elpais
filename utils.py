import json
import os


def save_to_json(data, browser_name="browser", os_name="os", suffix=None):
    os.makedirs("output", exist_ok=True)

    # Clean and format names
    browser_clean = browser_name.lower().replace(" ", "_")
    os_clean = os_name.lower().replace(" ", "_")

    # File name
    filename = f"el_pais_result_{os_clean}_{browser_clean}"
    if suffix is not None:
        filename += f"_{suffix}"
    filename += ".json"

    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
