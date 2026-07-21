import fitz
import chromadb
import os

# Read PDF
print("Reading PDF...")
doc = fitz.open("rag/documents/uae_labour_law.pdf")

# Extract text from each page
pages = []
for i, page in enumerate(doc):
    text = page.get_text()
    if text.strip():  # only add pages with text
        pages.append({
            "id": f"page_{i+1}",
            "text": text,
            "page": i+1
        })

print(f"Extracted {len(pages)} pages with text")

# Store in ChromaDB
print("Storing in ChromaDB...")
client = chromadb.PersistentClient(path="rag/vectorstore")
try:
    client.delete_collection("uae_documents")
except:
    pass

collection = client.create_collection("uae_documents")

collection.add(
    documents=[p["text"] for p in pages],
    ids=[p["id"] for p in pages],
    metadatas=[{"page": p["page"]} for p in pages]
)

print(f"✅ Stored {collection.count()} pages in ChromaDB")
print("RAG is ready!")
