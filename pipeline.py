from rag import run_research_pipeline


if __name__ == "__main__":
    topic = input("Enter a research topic: ").strip()
    if not topic:
        raise SystemExit("Please enter a research topic.")
    print(run_research_pipeline(topic)["report"])
