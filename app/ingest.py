import os
from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_DB_DIR = "chroma_store"

def load_documents(data_dir="data"):
    docs = []
    for root, _, files in os.walk(data_dir):
        for f in files:
            if f.endswith(".md") or f.endswith(".txt"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    docs.append(file.read())
    return docs

def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest():
    print("🔄 Starting ingestion...")

    docs = load_documents()

    if not docs:
        print("⚠️ No documents found in /data. Add .md or .txt files first.")
        return

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_or_create_collection("docs")

    for doc in docs:
        chunks = chunk_text(doc)
        embeds = model.encode(chunks).tolist()

        ids = [f"chunk_{i}" for i in range(len(embeds))]
        collection.add(ids=ids, embeddings=embeds, documents=chunks)

    print("✅ Ingestion complete! Stored embeddings in:", CHROMA_DB_DIR)


if __name__ == "__main__":
    ingest()
