# OpenLibrary Book Data Extraction

A simple Python exercise that uses the public [Open Library Search API](https://openlibrary.org/developers/api) to retrieve book data, filter the results by publication year, and save the complete returned records to a CSV file.

## Exercise

The goal of this exercise is to:

1. Request book data from the Open Library Search API.
2. Keep books whose `first_publish_year` is after 2000.
3. Retrieve up to 50 books.
4. Request all available fields from the API.
5. Save the results in a structured CSV file.

## Requirements

- Python 3.x
- `requests`

Install the required package with:

```bash
pip install requests
```

## How It Works

The script sends a request to:

```text
https://openlibrary.org/search.json
```

The main query parameters are:

```python
params = {
    "q": "first_publish_year:[2001 TO *]",
    "limit": 50,
    "fields": "*"
}
```

### Publication year filter

The query:

```text
first_publish_year:[2001 TO *]
```

uses Open Library's range-search syntax.

It means:

- minimum year: `2001`
- maximum year: no upper limit (`*`)

Therefore, only books with a `first_publish_year` from 2001 onward are returned.

### Number of results

```text
limit=50
```

requests up to 50 results.

### All fields

```text
fields=*
```

requests all available fields for each returned book.

Because different books may contain different fields, the script first collects the union of all field names:

```python
all_fields = set()

for book in books:
    all_fields.update(book.keys())
```

These field names are then used as the CSV column headers.

## Handling Complex Fields

Some API fields contain lists or dictionaries rather than simple values.

For example:

```json
{
    "author_name": [
        "J. K. Rowling"
    ]
}
```

CSV cells contain text values, so lists and dictionaries are converted to JSON strings before being written:

```python
def prepare_value(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value
```

This preserves the structure of those values while keeping the CSV valid.

## Output

The script creates:

```text
books.csv
```

The CSV contains:

- one row per book
- one column for every field found in the returned records
- UTF-8 encoding with BOM (`utf-8-sig`) for better compatibility with applications such as Microsoft Excel

## Run

Save the Python code as, for example:

```text
P1.py
```

Then run:

```bash
python P1.py
```

A successful run prints something similar to:

```text
50 books saved to books.csv.
XX columns created in CSV.
```

The exact number of columns depends on the fields returned by the API.

## Project Structure

```text
.
├── P1.py
├── books.csv
└── README.md
```

`books.csv` is the generated output file and does not need to be committed if the repository is intended to contain only the source code.

## API Reference

Open Library Search API:

https://openlibrary.org/developers/api

Open Library Search API documentation:

https://openlibrary.org/dev/docs/api/search
