"""Small, dependency-light extractive RAG pipeline."""

from collections import Counter
from math import log, sqrt
import re


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "by", "for", "from",
    "how", "in", "into", "is", "it", "of", "on", "or", "that", "the", "their",
    "this", "to", "was", "what", "when", "where", "which", "who", "why", "with",
}


def tokenize(text: str) -> list[str]:
    return [
        token for token in re.findall(r"[\w'-]{2,}", text.casefold())
        if token not in STOP_WORDS and not token.isdigit()
    ]


def split_chunks(text: str, max_chars: int = 850) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text).strip())
    chunks: list[str] = []
    current: list[str] = []
    size = 0

    for sentence in sentences:
        if not sentence:
            continue
        if current and size + len(sentence) > max_chars:
            chunks.append(" ".join(current))
            current, size = [], 0
        current.append(sentence[:max_chars])
        size += len(sentence)

    if current:
        chunks.append(" ".join(current))
    return chunks


def retrieve_passages(query: str, documents: list[dict[str, str]], limit: int = 6) -> list[dict[str, str]]:
    """Rank source passages with local TF-IDF cosine similarity."""
    query_counts = Counter(tokenize(query))
    candidates: list[dict[str, str]] = []
    for document in documents:
        for chunk in split_chunks(document.get("text", "")):
            if tokenize(chunk):
                candidates.append({
                    "title": document.get("title", "Source"),
                    "url": document.get("url", ""),
                    "text": chunk,
                })

    if not query_counts or not candidates:
        return []

    term_counts = [Counter(tokenize(candidate["text"])) for candidate in candidates]
    doc_frequency = Counter(term for counts in term_counts for term in counts)
    total = len(candidates)
    query_vector = {
        term: (1 + log(count)) * (log((total + 1) / (doc_frequency[term] + 1)) + 1)
        for term, count in query_counts.items()
        if doc_frequency[term]
    }
    query_norm = sqrt(sum(weight * weight for weight in query_vector.values()))
    if not query_norm:
        return []

    scored = []
    for candidate, counts in zip(candidates, term_counts):
        vector = {
            term: (1 + log(count)) * (log((total + 1) / (doc_frequency[term] + 1)) + 1)
            for term, count in counts.items()
            if term in query_vector
        }
        norm = sqrt(sum(weight * weight for weight in vector.values()))
        score = sum(query_vector[term] * weight for term, weight in vector.items())
        if norm and score:
            scored.append(({**candidate, "score": str(score / (query_norm * norm))}, score / (query_norm * norm)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return [candidate for candidate, _ in scored[:limit]]


def build_answer(topic: str, passages: list[dict[str, str]]) -> str:
    if not passages:
        return (
            f"# Research brief: {topic}\n\n"
            "No source passages matched the topic closely enough to form an evidence-based brief. "
            "Try a more specific search phrase or inspect the search notes below."
        )

    lines = [
        f"# Evidence brief: {topic}",
        "",
        "This extractive RAG brief ranks source passages locally with TF-IDF. Each point links to its source; "
        "open the original page to check context and recency.",
        "",
        "## Most relevant evidence",
    ]
    for passage in passages:
        excerpt = passage["text"].strip().replace("[", "(").replace("]", ")")
        lines.extend([
            f"- {excerpt}  ",
            f"  Source: [{passage['title']}]({passage['url']})",
        ])

    unique_sources = {}
    for passage in passages:
        unique_sources[passage["url"]] = passage["title"]
    lines.extend(["", "## Sources"])
    lines.extend(f"- [{title}]({url})" for url, title in unique_sources.items())
    return "\n".join(lines)


def run_research_pipeline(topic: str) -> dict[str, str]:
    """Run the RAG flow for command-line use."""
    from tools import scrape_url, web_search

    sources = web_search(topic)
    documents = []
    for source in sources[:3]:
        text = scrape_url(source["url"])
        if text:
            documents.append({**source, "text": text})
    scraped_urls = {document["url"] for document in documents}
    documents.extend({**source, "text": source["snippet"]} for source in sources if source["url"] not in scraped_urls)
    passages = retrieve_passages(topic, documents)
    return {"report": build_answer(topic, passages)}
