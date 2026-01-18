# Leitura e extração básica de dados do mod

import requests
from bs4 import BeautifulSoup

def extract_mod_data(url: str) -> dict:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1")
    title = title.get_text(strip=True) if title else None

    author = None
    meta_author = soup.find("meta", attrs={"name": "author"})
    if meta_author:
        author = meta_author.get("content")

    return {
        "url": url,
        "title": title,
        "author": author,
        "html": response.text
    }
