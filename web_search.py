from ddgs import DDGS


def web_search(query: str, max_results: int = 3):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", "")
            })

    return results
