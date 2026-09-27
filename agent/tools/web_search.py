from ddgs import DDGS

def web_search(query: str, max_results: int = 5):
    """
    Search the web for the given query.
    Returns a list of results. Each result has title, url, and snippet.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        # Clean the results so they are easy to use later
        cleaned = []
        for r in results:
            cleaned.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        return cleaned

    except Exception as e:
        # If something goes wrong, return an empty list + error message
        return [{"error": str(e)}]