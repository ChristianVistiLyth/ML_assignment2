import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,authors,year,citationCount,abstract,externalIds,url"

MIN_INTERVAL = 1.0
MAX_RETRIES = 5
_last_request = 0.0


def _get(params, headers):
    global _last_request
    for attempt in range(MAX_RETRIES):
        wait = MIN_INTERVAL - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()

        r = requests.get(URL, params=params, headers=headers, timeout=30)
        if r.status_code == 429 or r.status_code >= 500:
            backoff = 2 ** attempt
            time.sleep(backoff)
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()


def search_papers(topic, year_min=None, year_max=None,
                  min_citations=None, max_citations=None, limit=20):
    params = {"query": topic, "fields": FIELDS, "limit": limit}
    if year_min or year_max:
        params["year"] = f"{year_min or ''}-{year_max or ''}"
    if min_citations is not None:
        params["minCitationCount"] = min_citations

    #Optional apikey
    key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    headers = {"x-api-key": key} if key else {}

    r = _get(params, headers)
    papers = r.json().get("data", [])

    if max_citations is not None:
        papers = [p for p in papers if (p.get("citationCount") or 0) <= max_citations]

    result = []
    for p in papers:
        doi = (p.get("externalIds") or {}).get("DOI")
        result.append({
            "title": p.get("title"),
            "authors": [a["name"] for a in p.get("authors") or []],
            "year": p.get("year"),
            "citation_count": p.get("citationCount"),
            "url": f"https://doi.org/{doi}" if doi else p.get("url"),
            "abstract": p.get("abstract"),
        })
    return json.dumps(result)
