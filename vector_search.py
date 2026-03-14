import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def build_index(chunks):
    model = get_model()
    texts = [chunk["text"] for chunk in chunks]
    vectors = model.encode(texts, show_progress_bar=False)
    return np.array(vectors)

def find_relevant_chunks(question, chunks, vectors, top_k=3):
    model = get_model()
    question_vector = model.encode([question])
    scores = cosine_similarity(question_vector, vectors)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "page": chunks[idx]["page"],
            "score": round(float(scores[idx]), 3)
        })
    return results