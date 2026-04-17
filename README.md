# FastAPI Vector Search API

A minimal semantic search API using **FastAPI**, **Sentence Transformers**, and **FAISS**. It embeds documents, builds a vector index, and answers user queries via cosine/L2 similarity search.

---

## Features

- Semantic search with `sentence-transformers`
- Fast vector similarity search using FAISS
- Clean FastAPI router-based API
- Local model loading (offline-friendly)
- Section-based document chunking

---

## Tech Stack

- Python 3.9+
- FastAPI
- Uvicorn
- FAISS (CPU)
- sentence-transformers
- NumPy

---

## Project Structure

```
app/
├── main.py
├── api/
│   └── search.py
├── vector/
│   └── search.py
├── data/
│   ├── company_docs.txt
│   ├── docs.pkl
│   └── index.faiss
├── models/
│   └── all-MiniLM-L6-v2/
|   └── gpt2/
└── scripts/
    └── build_index.py
```

---

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### requirements.txt

```
fastapi
uvicorn
faiss-cpu
sentence-transformers
numpy
```

---

## Step 1: Prepare Documents

Add your content to:

```
app/data/company_docs.txt
```

Use section headers like:

```
Vision:
Our company focuses on...

Contact Info:
Email: example@company.com
```

---

## Step 2: Build Vector Index

Run the indexing script:

```bash
python -m app.vector.build_index
```

This will generate:

- `docs.pkl` → stored document chunks
- `index.faiss` → FAISS vector index

---

## Step 3: Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

## API Endpoint

### POST `/search`

**Request Body**

```json
{
  "question": "What is the company vision?"
}
```

**Response**

```json
{
  "answer": "Vision: Our company focuses on ..."
}
```

---

## How It Works

1. Documents are split into semantic sections
2. Each section is embedded using MiniLM
3. FAISS stores embeddings for fast similarity search
4. Query is embedded and searched against the index
5. Best-matching section is returned

---

## Notes

- Uses `IndexFlatL2` for simplicity
- `top_k` can be increased for multi-result search
- Model is loaded locally from `app/models/`
- Embedding model (all-MiniLM-L6-v2) and fallback model (gpt2) must be downloaded once from Hugging Face and saved locally under
  app/models/ 
- mkdir -p models
  cd models
  sudo apt install git-lfs
  git lfs install    
- git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2    
- git clone https://huggingface.co/openai-community/gpt2
- before running the API

---

## Next Improvements

- Add metadata (title, page, source)
- Return multiple results with scores
- Plug into Next.js frontend
- Add reranking (cross-encoder)

---

## License

MIT

