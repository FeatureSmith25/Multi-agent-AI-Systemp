import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

def web_search(query: str) -> list[dict[str, str]]:
    """Search the web for recent information and return titles, URLs, and snippets."""
    results = DDGS().text(query, max_results=5)
    return [
        {
            "title": result.get("title", "Untitled"),
            "url": result.get("href", result.get("url", "")),
            "snippet": result.get("body", result.get("content", ""))[:600],
        }
        for result in results
        if result.get("href") or result.get("url")
    ]

def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:12000]

    except Exception as e:
        return ""
