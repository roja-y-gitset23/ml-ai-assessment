# Core file: embeddings, cosine_similarity (own numpy code), semantic_search, keyword_search
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from faq_data import FAQS

QUESTIONS = [f[2] for f in FAQS]

model = SentenceTransformer("all-MiniLM-L6-v2")
faq_vectors = model.encode(QUESTIONS)          # shape: (12, 384) - one vector per FAQ question

STOPWORDS = {"i", "a", "an", "the", "is", "are", "am", "in", "on", "of", "to", "for", "from",
             "my", "me", "do", "how", "what", "when", "which", "who", "can", "or", "and", "if",
             "each", "am", "at", "by"}


def cosine_similarity(a, b):
    """cos(a, b) = (a . b) / (|a| * |b|)  - written by hand with numpy."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_search(query, top_k=3):
    q_vec = model.encode([query])[0]
    scores = [cosine_similarity(q_vec, v) for v in faq_vectors]
    order = np.argsort(scores)[::-1][:top_k]
    return [(int(i), float(scores[i])) for i in order]


def _words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS


def keyword_search(query, top_k=3):
    """Count how many query words appear (as exact words) in each FAQ question."""
    q_words = _words(query)
    results = []
    for i, question in enumerate(QUESTIONS):
        score = len(q_words & _words(question))
        if score > 0:
            results.append((i, score))
    results.sort(key=lambda x: -x[1])
    return results[:top_k]


# quick self-check of cosine_similarity
assert abs(cosine_similarity([1, 0], [1, 0]) - 1.0) < 1e-9
assert abs(cosine_similarity([1, 0], [0, 1])) < 1e-9