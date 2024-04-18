# CrawlX: Simple Page Data Extraction/Scraping API

CrawlX is an API that allows you to extract structured data from HTML documents or URLs using CSS selectors. It is particularly useful for frontend developers who need to scrape data from websites for various purposes such as web scraping, data mining, and content aggregation.

## Features

- Extract data from HTML documents or URLs using CSS selectors.
- Support for nested data extraction using nested selectors.
- Accepts both HTML content and URLs as input.

## Use Cases

- **Frontend Prototyping**: Frontend developers can use CrawlX for quick prototyping without the need to set up a backend server. They can easily integrate external data into their frontend applications and deploy them on serverless platforms like Netlify.

## How to Use

### Request Format

Send a POST request to `/extract` with the following JSON payload:

```json
{
    "html": "<html><body>...</body></html>",
    "selectors": {
        "key1": {
            "css": "selector1",
            "type": "text"
        },
        "key2": {
            "css": "selector2",
            "type": "text"
        },
        ...
    }
}
```

- `html` (optional): The HTML content to extract data from. Use either `html` or `url`.
- `url` (optional): The URL of the website to scrape. Use either `html` or `url`.
- `selectors`: A dictionary of CSS selectors to extract data from the HTML content.

### Response Format

The API will return a JSON response containing the extracted data:

```json
{
    "data": {
        "key1": "value1",
        "key2": "value2",
        ...
    }
}
```

## Example

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
-H "Content-Type: application/json" \
-d '{
    "html": "<div><h1>Hello, World!</h1><p>This is a sample HTML content</p></div>",
    "selectors": {
        "heading": {
            "css": "h1",
            "type": "text"
        },
        "paragraph": {
            "css": "p",
            "type": "text"
        }
    }
}'
```

CrawlX simplifies the process of web scraping and data extraction, making it easier to integrate external data into frontend applications.