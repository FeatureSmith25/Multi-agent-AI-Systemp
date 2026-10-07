import json
from typing import Iterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from rag import build_answer, retrieve_passages
from tools import scrape_url, web_search

app = FastAPI(title="ResearchMind API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)


def event(name: str, data: dict) -> str:
    return f"event: {name}\ndata: {json.dumps(data)}\n\n"


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "ResearchMind"}


@app.post("/api/research")
def research(request: ResearchRequest) -> StreamingResponse:
    topic = request.topic.strip()

    def run() -> Iterator[str]:
        try:
            yield event("stage", {"step": "search", "status": "running"})
            sources = web_search(topic)
            if not sources:
                raise RuntimeError("Free web search returned no results. Try a different topic.")
            search_text = "\n\n".join(
                f"Title: {source['title']}\nURL: {source['url']}\nSnippet: {source['snippet']}"
                for source in sources
            )
            yield event("stage", {"step": "search", "status": "done", "preview": search_text[:220]})

            yield event("stage", {"step": "reader", "status": "running"})
            documents = []
            for source in sources[:3]:
                text = scrape_url(source["url"])
                if text:
                    documents.append({**source, "text": text})
            # Search snippets keep retrieval useful when a site blocks scraping.
            scraped_urls = {document["url"] for document in documents}
            documents.extend(
                {**source, "text": source["snippet"]}
                for source in sources
                if source["url"] not in scraped_urls
            )
            reader_text = "\n\n".join(
                f"{document['title']} ({document['url']})\n{document['text'][:900]}"
                for document in documents[:6]
            )
            yield event("stage", {"step": "reader", "status": "done", "preview": reader_text[:220]})

            yield event("stage", {"step": "retrieve", "status": "running"})
            passages = retrieve_passages(topic, documents)
            yield event("stage", {"step": "retrieve", "status": "done"})

            yield event("stage", {"step": "answer", "status": "running"})
            report = build_answer(topic, passages)
            yield event("stage", {"step": "answer", "status": "done"})
            yield event("complete", {
                "topic": topic,
                "report": report,
                "search": search_text,
                "reader": reader_text,
            })
        except Exception as exc:
            yield event("error", {"message": str(exc) or "The research pipeline could not be completed."})

    return StreamingResponse(run(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "X-Accel-Buffering": "no"
    })


app.mount("/", StaticFiles(directory="web", html=True), name="web")
