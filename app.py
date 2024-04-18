from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx as requests
from selectorlib import Extractor
import yaml

app = FastAPI()

# Request body model
class SelectorRequest(BaseModel):
    html: str = None
    url: str = None
    selectors: dict

# Response body model
class ExtractionResponse(BaseModel):
    data: dict

@app.post("/extract", response_model=ExtractionResponse)
async def extract_data(request: SelectorRequest):
    """
    # Simple Page Data Extraction/Scraping API
    Used to Scrape data from a HTML Document/URL Provided. Selectors needs to be Provided to Extract and Format the Data Accordingly.
    A Sample Request Body has been Provided Below
    ```json
    {
        "url": "https://www.scrapethissite.com/pages/simple/",
        "selectors": {
            "countries": {
                "css": "div.country",
                "type": "Text",
                "multiple": true,
                "children": {
                    "name": {
                        "css": "h3.country-name",
                        "type": "Text"
                    },
                    "info": {
                        "css": "div.country-info",
                        "type": "Text",
                        "children": {
                            "capital": {
                                "css": "span.country-capital",
                                "type": "Text"
                            },
                            "population": {
                                "css": "span.country-population",
                                "type": "Text"
                            },
                            "area": {
                                "css": "span.country-area",
                                "type": "Text"
                            }
                        }
                    }
                }
            }
        }
    }
    ```
    """
    # Check if either html or url is provided
    if not request.html and not request.url:
        raise HTTPException(status_code=400, detail="Either 'html' or 'url' must be provided")

    # If url is provided, fetch the HTML content
    if request.url:
        response = requests.get(request.url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch URL")

        html = response.text
    else:
        html = request.html

    # Convert selectors from JSON to YAML
    selectors_yaml = yaml.dump(request.selectors)

    # Extract data using Selectorlib
    extractor = Extractor.from_yaml_string(selectors_yaml)
    extracted_data = extractor.extract(html)

    return {"data": extracted_data}
