import chromadb
import requests

# Connect to ChromaDB
client = chromadb.PersistentClient(path="rag/vectorstore")
collection = client.get_collection("uae_documents")

# User question
question = "How many days of annual leave is an employee entitled to?"

# Search ChromaDB for relevant pages
results = collection.query(
    query_texts=[question],
    n_results=3
)

# Combine relevant pages into context
context = "\n\n".join(results['documents'][0])

# Send to Ollama with context
prompt = f"""You are a UAE Labour Law expert.
Use only the following law content to answer the question.
Always mention which page the answer comes from.

Law Content:
{context}

Question: {question}

Give a clear short answer."""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
)

print(f"Question: {question}")
print(f"\nAnswer: {response.json()['response']}")