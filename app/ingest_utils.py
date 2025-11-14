import nltk

# Ensure tokenizer resources exist
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


import os
from typing import List

import chromadb
from sentence_transformers import SentenceTransformer
import trafilatura

CHROMA_DB_DIR = "chroma_store"
COLLECTION_NAME = "docs"

# Reuse the same model and collection as rag.py / ingest.py
_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
_collection = _client.get_or_create_collection(COLLECTION_NAME)


import nltk
from nltk.tokenize import sent_tokenize
from typing import List

def semantic_chunk(text: str, max_tokens: int = 120, overlap: int = 20) -> List[str]:
    """
    Semantic chunking using sentence boundaries + overlap.
    Approx token estimate: num_words / 0.75
    """
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        sentence_len = len(words)

        if current_length + sentence_len <= max_tokens:
            current_chunk.append(sentence)
            current_length += sentence_len
        else:
            chunks.append(" ".join(current_chunk))

            # Start new chunk with overlap
            overlap_sentences = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s.split()) for s in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks



def ingest_text(name: str, text: str) -> int:
    """
    Ingest a block of raw text into Chroma as multiple chunks.
    Returns the number of chunks added.
    """
    chunks = semantic_chunk(text)
    if not chunks:
        return 0

    embeddings = _model.encode(chunks).tolist()
    ids = [f"{name}_{i}" for i in range(len(chunks))]

    _collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
    )

    return len(chunks)


def ingest_url(url: str) -> int:
    """
    Download a webpage and ingest its main text content.
    Returns number of chunks added.
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return 0

    text = trafilatura.extract(downloaded)
    if not text:
        return 0

    # Use a sanitized version of the URL as a base name
    safe_name = (
        url.replace("https://", "")
           .replace("http://", "")
           .replace("/", "_")
           .replace("?", "_")
           .replace("&", "_")
    )

    return ingest_text(safe_name, text)


def list_all_docs() -> List[str]:
    """
    Debug helper: list all stored documents (chunks) in the collection.
    """
    all_docs = _collection.get()
    return all_docs.get("documents", [])
