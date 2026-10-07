# ResearchMind — free RAG research

ResearchMind is a small retrieval-augmented research app. It searches the web with DDGS, fetches a few result pages, ranks passages locally with TF-IDF, and builds a brief with links to the sources.

It does not use Ollama, a hosted language model, or paid API keys. The answer is extractive: it presents relevant source passages rather than generating new prose with an LLM. Web search requires an internet connection and public search providers may rate-limit requests.

## Run on Windows

1. Create and activate a virtual environment if you do not already have one:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   python -m uvicorn api:app --reload
   ```

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

No `.env` file is required. The command-line version is also available with `python pipeline.py`.

## API

- `GET /api/health` reports whether the app is running.
- `POST /api/research` accepts `{"topic": "..."}` and streams search, reading, retrieval, and answer progress.
