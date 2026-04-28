# RAG-based Mutual Fund FAQ Chatbot — Full Plan

## 1. Project Overview

Build a **facts-only FAQ chatbot** that answers questions about mutual fund schemes using **RAG (Retrieval-Augmented Generation)**. Every answer must include **one official source link**. No investment advice.

**Target users:** Retail investors comparing schemes, and support/content teams handling repetitive MF questions.

---

## 2. Product & AMC Selection

| Item | Choice |
|------|--------|
| Platform | **Groww** |
| AMC | **SBI Mutual Fund** |

### Schemes (3–5)
- SBI Bluechip Fund (Large Cap)
- SBI Flexicap Fund
- SBI Long Term Equity Fund (ELSS)
- SBI Small Cap Fund

---

## 3. Data Collection (15–25 URLs)

Collect **only official public pages** from:

### AMC Website (sbimf.com)
- Scheme factsheets
- KIM (Key Information Memorandum)
- SID (Scheme Information Document)
- Fee/charges pages

### Official Regulators
- **AMFI** — https://www.amfiindia.com
- **SEBI** — https://www.sebi.gov.in

### Topics to Cover
- Expense ratio
- Exit load rules
- Minimum SIP
- ELSS lock-in (3 years)
- Riskometer explanation
- Benchmark details
- Statement / tax-doc download guides

---

## 4. RAG Architecture

```
User Question
     ↓
Retriever (FAISS / Chroma)
     ↓
Relevant Chunks
     ↓
LLM (GPT)
     ↓
Answer + Source Link
```

---

## 5. Tech Stack

- **Language:** Python
- **Framework:** LangChain
- **LLM:** OpenAI (or local LLM)
- **Vector DB:** FAISS
- **UI:** Streamlit

### Install
```bash
pip install langchain openai faiss-cpu streamlit tiktoken
```

---

## 6. Implementation Steps

### Step 1 — Load & Index Data
- Use `WebBaseLoader` to fetch the 15–25 URLs.
- Split documents using `RecursiveCharacterTextSplitter` (chunk size 500, overlap 50).
- Generate embeddings with `OpenAIEmbeddings`.
- Store in `FAISS` vector DB.

### Step 2 — Build Retrieval QA Chain
- Use `RetrievalQA` with `ChatOpenAI` (`temperature=0` for factual output).
- Retriever pulls top relevant chunks for each query.

### Step 3 — System Prompt (Facts-Only Rules)
```
You are a Mutual Fund FAQ assistant.

Rules:
- Answer only factual questions
- Max 3 sentences
- Always include ONE source link
- No investment advice
- If opinion question → refuse politely

Refusal:
"I can only provide factual information, not investment advice.
 Please refer to official sources: <link>"
```

### Step 4 — Refusal Logic
Detect opinion-based queries by keywords:
- `"should I"`, `"best fund"`, `"invest"`, `"buy"`, `"sell"`
- If matched → return safe-refusal message with educational link.

### Step 5 — Streamlit UI
- Title: **📊 Mutual Fund FAQ Bot**
- Welcome line: *"Facts-only. No investment advice."*
- Show 3 example questions:
  - What is expense ratio?
  - What is exit load?
  - What is the ELSS lock-in period?
- Text input box → call QA chain → display answer + source.

---

## 7. Critical Rules

### ✅ Must Do
- Use **only official sources** (AMC / SEBI / AMFI).
- Include **at least 1 source link** per answer.
- Keep answers **≤ 3 sentences**.
- End with: *"Last updated from sources: <date>"*.

### ❌ Must NOT Do
- Do **NOT** collect personal data (PAN, Aadhaar, OTP, email, phone, account numbers).
- Do **NOT** calculate or compare returns.
- Do **NOT** give investment advice.
- Do **NOT** use third-party blogs as sources.
- Do **NOT** screenshot the app back-end.

---

## 8. Sample Q&A

**Q:** What is the ELSS lock-in period?
**A:** ELSS schemes have a lock-in period of 3 years.
*Source:* https://www.amfiindia.com

**Q:** Should I invest in SBI Bluechip?
**A:** I can only provide factual information, not investment advice. Please refer to official sources: https://www.amfiindia.com

---

## 9. Deliverables

1. **Working prototype** — app or notebook (or ≤3-min demo video if not hostable).
2. **Source list** — CSV/MD with the 15–25 URLs used.
3. **README** — setup steps, AMC + scheme scope, known limits.
4. **Sample Q&A file** — 5–10 queries with assistant's answers + links.
5. **Disclaimer snippet** — "Facts-only. No investment advice."

---

## 10. README Template

```
Project: Mutual Fund FAQ Chatbot
AMC: SBI Mutual Fund
Schemes: Bluechip, Flexicap, ELSS, Small Cap

Setup:
  pip install -r requirements.txt
  streamlit run app.py

Limits:
  - No investment advice
  - Small dataset (15–25 official pages)
  - Facts-only answers
```

---

## 11. Skills Being Evaluated

| Skill | Focus |
|-------|-------|
| **W1 — Model Thinking** | Identify the exact fact asked; decide answer vs. refuse |
| **W2 — LLMs & Prompting** | Clear instructions, concise phrasing, polite refusals, citations |
| **W3 — RAG** | Small-corpus retrieval with accurate citations from AMC/SEBI/AMFI |

---

## 12. Three Most Important Things

1. **Correct source link** in every answer.
2. **Strict refusal logic** for opinion questions.
3. **Short, factual answers** (≤ 3 sentences).
