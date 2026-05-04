import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,authors,year,citationCount,abstract,externalIds,url"

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

    r = requests.get(URL, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    papers = r.json().get("data", [])

    if max_citations is not None:
        papers = [p for p in papers if (p.get("citationCount") or 0) <= max_citations]
    return papers

if __name__ == "__main__":
    from pprint import pprint
    pprint(search_papers("retrieval-augmented generation", year_max=2020, limit=3))