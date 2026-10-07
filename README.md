# ResearchMind RAG 🔎

> **Search the web. Retrieve relevant evidence. Follow the sources.**

**ResearchMind RAG** is a source-led research assistant that helps users investigate a topic by searching the web, retrieving relevant source content, ranking useful passages locally, and presenting the results as a clear **evidence brief with links to original sources**.

🌐 **Live Demo:** https://researchmind-rag.onrender.com/

---

## 📌 Overview

Finding reliable information on the web often requires visiting multiple websites, reading long pages, identifying useful passages, and connecting the evidence back to its original sources.

ResearchMind simplifies this workflow.

Instead of giving users an unsupported AI-generated answer, the application focuses on:

- 🔎 Web search
- 📄 Source retrieval
- 🧩 Relevant passage extraction
- 📊 Local relevance ranking
- 🔗 Source traceability
- 📝 Evidence-based research briefs

The goal is simple:

> **Search → Read → Retrieve → Cite**

---

## ✨ Features

### 🔎 1. Web Search

Users can enter a research question or topic and search the web for relevant information.

Example:

```text
How is AI changing drug discovery?
```

The system finds relevant web pages and search snippets related to the query.

---

### 📖 2. Source Reading

ResearchMind retrieves relevant web pages and collects source content for further processing.

Instead of relying only on search snippets, the system attempts to work with the actual source material.

---

### 🧠 3. Local Evidence Retrieval

Relevant passages are identified and ranked locally using **TF-IDF-based retrieval**.

This allows the system to determine which passages are most relevant to the user's research query without requiring a hosted LLM API.

---

### 📊 4. Evidence Ranking

Retrieved passages are ranked according to their relevance to the user's query.

This makes it easier to identify the most useful pieces of information from multiple sources.

---

### 🔗 5. Source Traceability

ResearchMind keeps the connection between retrieved evidence and its original webpage.

Users can therefore follow the source links and verify the information themselves.

---

### 📝 6. Evidence Brief

The final research output is presented as a concise evidence-oriented brief containing relevant findings and source references.

This makes the system useful for:

- Research
- Technical investigation
- Literature exploration
- Fact finding
- Topic exploration
- Early-stage academic research

---

## ⚙️ How It Works

ResearchMind follows a four-stage research workflow:

```text
                  USER QUESTION
                       │
                       ▼
              ┌─────────────────┐
              │   1. WEB SEARCH │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  2. READ SOURCES│
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ 3. RETRIEVE     │
              │    EVIDENCE     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ 4. BUILD BRIEF  │
              └────────┬────────┘
                       │
                       ▼
             EVIDENCE + SOURCE LINKS
```

The deployed application describes the workflow as:

1. **Search the web**
2. **Read sources**
3. **Retrieve evidence**
4. **Build brief**


---

## 🧩 RAG Architecture

ResearchMind follows a lightweight Retrieval-Augmented Generation-style research workflow.

```text
User Query
    │
    ▼
Web Search
    │
    ▼
Search Results
    │
    ▼
Source Retrieval
    │
    ▼
Text Extraction
    │
    ▼
Text Chunking
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Similarity / Relevance Ranking
    │
    ▼
Top Evidence Passages
    │
    ▼
Evidence Brief
    │
    ▼
Original Source Links
```

### Why local retrieval?

A major design goal of ResearchMind is reducing dependence on expensive hosted AI APIs.

The deployed application specifically identifies its retrieval layer as **local TF-IDF retrieval** and states that no hosted language model is used for this process.

---

## 🧠 Retrieval Approach

### TF-IDF

ResearchMind uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to estimate how relevant a passage is to a query.

The basic idea is:

```text
TF-IDF = Term Frequency × Inverse Document Frequency
```

Words that are important to a particular document/query receive higher relevance than words that appear everywhere.

This provides a lightweight and explainable retrieval mechanism.

---

## 🔍 Example Workflow

Suppose the user enters:

```text
How is AI changing drug discovery?
```

ResearchMind can perform the following process:

### Step 1 — Search

Find relevant webpages related to AI and drug discovery.

### Step 2 — Retrieve

Fetch useful content from the discovered sources.

### Step 3 — Process

Clean and prepare the retrieved text.

### Step 4 — Rank

Use local TF-IDF retrieval to identify passages most relevant to the query.

### Step 5 — Build

Combine the retrieved evidence into a research brief.

### Step 6 — Verify

Provide links to the original sources so the user can inspect the evidence.

---

## 🏗️ Project Architecture

A conceptual architecture looks like this:

```text
┌───────────────────────────────┐
│           Frontend            │
│                               │
│  Query Input                  │
│  Research Controls             │
│  Evidence Brief                │
│  Source Links                  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          Backend API          │
│                               │
│  Query Processing             │
│  Search Orchestration         │
│  Source Retrieval             │
│  Evidence Processing          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Retrieval Engine        │
│                               │
│  Text Cleaning                │
│  Chunking                     │
│  TF-IDF Vectorization         │
│  Relevance Ranking            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Research Output        │
│                               │
│  Evidence                     │
│  Source Notes                 │
│  Original URLs                │
└───────────────────────────────┘
```

---

## 🎯 Project Goals

ResearchMind is designed around several principles:

### 1. Evidence First

Information should be connected to identifiable sources.

### 2. Transparency

Users should be able to inspect where information came from.

### 3. Lightweight Architecture

The retrieval system should work without requiring an expensive hosted LLM.

### 4. Reproducible Research

The research process should be understandable and repeatable.

### 5. Simple User Experience

Users should be able to enter a question and obtain a useful evidence brief without dealing with complex research tooling.

---

## 🛠️ Technology Stack

> Update this section with the exact libraries from your repository if they differ.

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- REST API / server-side application

### Information Retrieval

- TF-IDF
- Text processing
- Similarity-based ranking

### Data Sources

- Open web sources
- Retrieved webpages
- Search results

### Deployment

- Render

---

## 📁 Suggested Project Structure

```text
researchmind-rag/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── retrieval/
│   └── utils/
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── templates/
│   └── index.html
│
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── ...
```

> Adjust this structure to match your actual repository.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- Git
- pip
- A web-search/data-source API if your implementation requires one

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/researchmind-rag.git
```

Move into the project directory:

```bash
cd researchmind-rag
```

---

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file if your project requires environment variables.

Example:

```env
SEARCH_API_KEY=your_api_key
```

Never commit secrets or API keys to GitHub.

---

### 5. Run the Application

Use the command appropriate to your backend.

For example:

```bash
python app.py
```

or:

```bash
uvicorn app:app --reload
```

Then open the local URL shown by your server.

---

## 🌐 Live Demo

Try ResearchMind here:

**https://researchmind-rag.onrender.com/**

The current deployed interface provides a research workspace where users can enter a question, run the research workflow, and receive an evidence-oriented result with source links.

---

## 💡 Example Research Questions

ResearchMind can be used to explore questions such as:

```text
How is AI changing drug discovery?
```

```text
What are the latest approaches to fusion energy?
```

```text
How is CRISPR gene editing being used in medicine?
```

```text
What are the major challenges in AI healthcare?
```

```text
What are the current approaches to carbon capture?
```

---

## 🔐 Privacy & API Design

ResearchMind is designed around a lightweight research workflow.

The deployed application describes the session as a **private session** and emphasizes source-led research rather than relying on a paid AI API.

If you extend the project, consider implementing:

- Secure API key management
- Request validation
- Rate limiting
- Input sanitization
- HTTPS
- Secure logging
- Source validation
- Protection against malicious webpages

---

## ⚠️ Limitations

ResearchMind should not be treated as an automatic guarantee of factual correctness.

Potential limitations include:

- Search engine result quality
- Webpage availability
- Dynamic webpages
- Incorrect or misleading source content
- TF-IDF's limited semantic understanding
- Duplicate information across sources
- Paywalled or inaccessible webpages
- Poorly structured webpage content

Always verify important information against the original sources.

---

## 🚧 Future Improvements

ResearchMind can be extended significantly.

### 🧠 Semantic Retrieval

Replace or complement TF-IDF with embeddings and vector search.

Possible technologies:

- Sentence Transformers
- FAISS
- ChromaDB
- Qdrant
- pgvector

---

### 🤖 Optional LLM Layer

An optional LLM could be added for:

- Evidence summarization
- Question answering
- Source comparison
- Contradiction detection
- Automatic report generation

Importantly, the retrieval layer can remain independent from the LLM.

---

### 📚 Multi-Document Research

Support deeper research across multiple documents:

```text
Question
   ↓
Search
   ↓
10–20 Sources
   ↓
Extract Evidence
   ↓
Rank Evidence
   ↓
Compare Sources
   ↓
Generate Research Report
```

---

### ⚖️ Source Comparison

Future versions could automatically identify:

```text
Source A → supports claim
Source B → contradicts claim
Source C → provides additional evidence
```

This would make the application more useful for serious research.

---

### 📈 Research Quality Score

A future version could score sources based on:

- Relevance
- Source authority
- Recency
- Evidence density
- Cross-source agreement

---

## 📊 Why This Project Is Interesting

ResearchMind demonstrates several important concepts in modern data and AI engineering:

- Information retrieval
- Natural language processing
- Search systems
- Text preprocessing
- TF-IDF
- Ranking algorithms
- Web data extraction
- Evidence-based systems
- Backend API development
- Full-stack application development
- Deployment

For someone building a **Data Science / AI Engineering portfolio**, this project demonstrates more than simply calling an AI API—it shows how a retrieval pipeline can be designed and deployed.

---

## 🎓 Learning Outcomes

By building ResearchMind, you can learn:

### Data Science

- Text preprocessing
- Feature extraction
- TF-IDF
- Similarity scoring
- Ranking

### NLP

- Tokenization
- Stop-word handling
- Text normalization
- Document representation
- Information retrieval

### Software Engineering

- API design
- Modular architecture
- Error handling
- Environment variables
- Testing

### AI Engineering

- RAG concepts
- Retrieval pipelines
- Evidence grounding
- Source attribution
- Hybrid search architectures

### Deployment

- Git/GitHub
- Environment configuration
- Cloud deployment
- Production debugging

---

## 🤝 Contributing

Contributions are welcome.

### Fork the repository

```bash
git fork
```

### Create a feature branch

```bash
git checkout -b feature/new-feature
```

### Commit your changes

```bash
git commit -m "Add new feature"
```

### Push the branch

```bash
git push origin feature/new-feature
```

Then open a Pull Request.

---

## 🐛 Reporting Issues

If you find a bug or have an improvement idea, open a GitHub Issue with:

- Problem description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs if applicable

---

## 📄 License

Add your project's license here.

For example:

```text
MIT License
```

If you have not selected a license yet, choose one appropriate for your project before publishing the repository.

---

## 👨‍💻 Author

**Hardik Sachan**

Data Science & AI Engineering Enthusiast

Building practical projects around:

- Data Science
- Machine Learning
- NLP
- RAG
- AI Engineering
- Information Retrieval

---

## ⭐ Support

If you find this project useful:

⭐ Star the repository  
🍴 Fork the project  
🐛 Report issues  
💡 Suggest improvements  

---

## 🔗 Project Links

- **Live Application:** https://researchmind-rag.onrender.com/
- **GitHub Repository:** Add your repository URL here
- **Portfolio:** Add your portfolio URL here

---

## 🧠 Core Idea

> **ResearchMind doesn't just search for information. It helps users find evidence, understand where that evidence came from, and follow the original sources.**

**SEARCH → READ → RETRIEVE → CITE**