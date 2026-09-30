import csv
import json

import requests


API_URL = "https://openlibrary.org/search.json"
OUTPUT_FILE = "books.csv"

params = {
    "q": "first_publish_year:[2001 TO *]",
    "limit": 50,
    "fields": "*",
}

response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

books = data.get("docs", [])


# Collect all fields that appear in the returned books
all_fields = set()

for book in books:
    all_fields.update(book.keys())

# Sort field names to create consistent CSV columns
all_fields = sorted(all_fields)


# Convert complex values such as lists and dictionaries to JSON strings
def prepare_value(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)

    return value


# Write the book data to a CSV file
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=all_fields,
        extrasaction="ignore",
    )

    writer.writeheader()

    for book in books:
        row = {
            field: prepare_value(book.get(field, ""))
            for field in all_fields
        }

        writer.writerow(row)


print(f"{len(books)} books saved to {OUTPUT_FILE}.")
print(f"{len(all_fields)} columns created in CSV.")

