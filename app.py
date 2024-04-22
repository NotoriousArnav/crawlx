from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from selectorlib import Extractor
from pydantic import BaseModel
import httpx as requests
import yaml

app = FastAPI()

origins = ["*"]
 
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

# Request body model
class SelectorRequest(BaseModel):
    html: str = None
    url: str = None
    selectors: dict

# Response body model
class ExtractionResponse(BaseModel):
    data: dict

@app.get('/')
async def index():
    """
    # Index Page of the API
    """
    return {
        "message": [
            """Welcome to CrawlX API""", 
            """Use /docs to Know More about the API Endpoints""",
            """Demo project at https://notoriousarnav.github.io/simple_alpine_axios_prj/""",
            """Source Code Available at https://github.com/NotoriousArnav/crawlx"""
        ]
    }

@app.post("/extract", response_model=ExtractionResponse)
async def extract_data(request: SelectorRequest):
    """
    # Simple Page Data Extraction/Scraping API
    Used to Scrape data from a HTML Document/URL Provided. Selectors needs to be Provided to Extract and Format the Data Accordingly.
    """
    # Check if either html or url is provided
    if not request.html and not request.url:
        raise HTTPException(status_code=400, detail="Either 'html' or 'url' must be provided")

    # If url is provided, fetch the HTML content
    if request.url:
        response = requests.get(
                    request.url,
                    headers = headers
                )
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
