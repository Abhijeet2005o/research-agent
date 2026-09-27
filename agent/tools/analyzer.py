from collections import Counter
import re

# Common words we ignore
STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "this", "that", "it", "as", "by", "from",
    "at", "be", "will", "has", "have", "its", "their", "new", "last", "week"
}

def tokenize(text: str):
    """Turn text into a list of meaningful words."""
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def rank_results(query: str, results: list):
    """
    Score each result based on how many query words appear in it.
    Returns a new list sorted by score (highest first).
    """
    query_words = set(tokenize(query))
    scored = []

    for r in results:
        if "error" in r:
            continue

        text = r.get("title", "") + " " + r.get("snippet", "")
        text_words = set(tokenize(text))

        # Count how many query words appear
        overlap = query_words.intersection(text_words)
        score = len(overlap)

        # Small bonus if words appear in the title
        title_words = set(tokenize(r.get("title", "")))
        if query_words.intersection(title_words):
            score += 0.5

        scored.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", ""),
            "score": score
        })

    # Sort highest score first
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def top_keywords(results: list, n: int = 8):
    """Find the most common important words across all results."""
    counter = Counter()
    for r in results:
        if "error" in r:
            continue
        text = r.get("title", "") + " " + r.get("snippet", "")
        counter.update(tokenize(text))
    return [word for word, _ in counter.most_common(n)]