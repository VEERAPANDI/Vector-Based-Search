import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_PATH = "app/data/index.faiss"
DOCS_PATH = "app/data/docs.pkl"

model = SentenceTransformer("app/models/all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

with open(DOCS_PATH, "rb") as f:
    docs = pickle.load(f)

# Lower = more strict, Higher = broader
CONFIDENCE_GAP_THRESHOLD = 0.08
MAX_RESULTS = 5
MIN_RESULTS = 3


def vector_search(query: str):
    query_vec = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Always search with higher top_k
    scores, indices = index.search(query_vec, MAX_RESULTS)

    results = []

    base_score = scores[0][0]

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        # Stop if relevance drops too much
        if abs(score - base_score) > CONFIDENCE_GAP_THRESHOLD:
            break

        results.append({
            "text": docs[idx],
            "score": float(score)
        })

    # Guarantee minimum results
    if len(results) < MIN_RESULTS:
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = {
                "text": docs[idx],
                "score": float(score)
            }
            if item not in results:
                results.append(item)
            if len(results) >= MIN_RESULTS:
                break

    return {
        "source": "faiss",
        "results": results
    }
