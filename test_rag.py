import chromadb

# Connect to ChromaDB
client = chromadb.PersistentClient(path="rag/vectorstore")
collection = client.get_collection("uae_documents")

# Ask a question
question = "What is annual leave entitlement?"

# Search ChromaDB
results = collection.query(
    query_texts=[question],
    n_results=3
)

# Show what it found
print(f"Question: {question}")
print(f"\nFound {len(results['documents'][0])} relevant pages:")

for i, doc in enumerate(results['documents'][0]):
    page_num = results['metadatas'][0][i]['page']
    print(f"\nPage {page_num}:")
    print(doc[:200])