# How the Bot Finds Answers

The RAG (Retrieval-Augmented Generation) flow used in this project.

---

## 1. Build phase (one-time, on first run)

**`rag_engine.py` → `build_or_load_index()`**

```
21 official URLs (sources.py)
   │
   │  WebBaseLoader   ← fetches HTML, strips tags
   ▼
21 Documents (one per page)
   │
   │  RecursiveCharacterTextSplitter(chunk_size=500, overlap=50)
   ▼
284 small text chunks  (each keeps source URL in metadata)
   │
   │  OpenAIEmbeddings(text-embedding-3-large, dim=1536)
   ▼
284 vectors of 1536 floats
   │
   │  FAISS.from_documents(...)
   ▼
.faiss_index/   ← saved to disk, reused on next run
```

Each chunk is now a point in a 1536-dimensional space where
**semantically similar text sits close together**.

---

## 2. Query phase (every question)

**User asks:** *"What is the ELSS lock-in period?"*

```
Question
   │
   │  same OpenAIEmbeddings model
   ▼
1 vector of 1536 floats         (the question's embedding)
   │
   │  db.as_retriever(search_kwargs={"k": 4})
   │  FAISS does L2 nearest-neighbour search
   ▼
Top 4 most-similar chunks  (e.g., from investor.sebi.gov.in/elss.html)
   │
   │  stuffed into the prompt as `{context}`
   ▼
PromptTemplate (prompts.py SYSTEM_PROMPT)
   │
   ▼
ChatOpenAI(model="gpt-4o", temperature=0)
   │
   ▼
Final answer  +  Source URL  +  "Last updated from sources: …"
```

---

## 3. Why this works without "real" search

- **Keyword search** would miss synonyms — *"lock-in"* vs *"tenure"* vs
  *"redemption restriction"*.
- **Embeddings** map sentences with the same *meaning* to similar vectors,
  so a question phrased any way still retrieves the right chunk.
- The LLM never invents facts — it can only summarise the 4 chunks it
  received. That's why every answer cites a URL from the corpus, not the
  open web.

---

## 4. Pre-filter before the LLM

Before any of the above runs, **`refusal.py`** runs inside `app.py`:

- `contains_pii(q)` → blocks PAN / Aadhaar / email / phone / OTP locally;
  nothing leaves the box.
- `is_opinion(q)` → returns the canned refusal; the LLM is **not** called.

So opinion / PII questions never reach OpenAI — saves cost and guarantees
no advice slips through.

---

## TL;DR

> **Embed the question → cosine-nearest 4 chunks from FAISS → stuff into a
> strict-rules prompt → gpt-4o writes the answer with a plain-text source URL.**

---

## Key files

| File | Role |
|------|------|
| `sources.py`     | The 21 official URLs ingested |
| `rag_engine.py`  | Loader, splitter, FAISS index, retrieval QA chain |
| `prompts.py`     | System prompt with formatting rules |
| `refusal.py`     | Opinion / PII pre-filter |
| `app.py`         | Streamlit UI |
| `.faiss_index/`  | Cached vector index (built once, reused) |
