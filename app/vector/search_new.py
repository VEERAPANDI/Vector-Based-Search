import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_PATH = "app/data/index.faiss"
DOCS_PATH = "app/data/docs.pkl"

model = SentenceTransformer("app/models/all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

with open(DOCS_PATH, "rb") as f:
    docs = pickle.load(f)

# ----------------------------------
# Intent detection (lightweight)
# ----------------------------------
CODE_KEYWORDS = {
    "function", "error", "bug", "php", "laravel",
    "controller", "helper", "upload", "api",
    "calculate", "trade", "image", "code related", "format"
}

def detect_intent(query: str) -> str:
    q = query.lower()
    for word in CODE_KEYWORDS:
        if word in q:
            return "code"
    return "company"

# ----------------------------------
# Improved vector search
# ----------------------------------
def vector_search(query: str, top_k: int = 5):
    intent = detect_intent(query)

    print(f"Detected intent: {intent}")

    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, top_k)

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        doc = docs[idx]

        # Attach distance for ranking
        doc_with_score = dict(doc)
        doc_with_score["_distance"] = float(dist)

        results.append(doc_with_score)

    # ----------------------------------
    # Filter by intent + distance
    # ----------------------------------
    if intent == "code":
        filtered = [
            r for r in results
            if r.get("source") == "code" and r["_distance"] < 1.0
        ]
    else:
        filtered = [
            r for r in results
            if r.get("source") == "company" and r["_distance"] < 1.2
        ]

    # ----------------------------------
    # Sort best result first
    # ----------------------------------
    filtered.sort(key=lambda x: x["_distance"])

    # ----------------------------------
    # Fallback if nothing matched
    # ----------------------------------
    if not filtered:
        return []

    return filtered