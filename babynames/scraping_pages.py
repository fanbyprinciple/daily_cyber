import requests
from bs4 import BeautifulSoup
import json

# Base URL format (page numbers change)
base_url = "https://www.mamanatural.com/baby-names/girls/origins/indian-sanskrit-girl-names/page/{}/"

# List to store names
names_data = []

# Loop through pages 1 to 18
for page in range(1, 19):
    url = base_url.format(page)
    print(f"Scraping: {url}")

    # Send request
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Skipping page {page} (Error {response.status_code})")
        continue

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all name rows
    for row in soup.find_all("tr", class_="post name-item name-item-girl"):
        try:
            # Extract name
            name = row.find("th", class_="name").find("strong").text.strip()

            # Extract meaning
            meaning_tag = row.find("td", class_="meaning").find("small")
            meaning = meaning_tag.text.strip() if meaning_tag else "Meaning not available"

            # Store in list
            names_data.append({"name": name, "meaning": meaning})

        except AttributeError:
            continue  # Skip row if data is missing

# Save to JSON
with open("sanskrit_names.json", "w", encoding="utf-8") as f:
    json.dump(names_data, f, indent=4, ensure_ascii=False)

print(f"Scraping complete! {len(names_data)} names saved in 'sanskrit_names.json'.")
