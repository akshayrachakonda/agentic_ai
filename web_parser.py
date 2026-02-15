import requests
from bs4 import BeautifulSoup
import time


def parse_webpage(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Research Agent)"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove junk
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Rate limit
    time.sleep(2)

    return " ".join(text.split())
