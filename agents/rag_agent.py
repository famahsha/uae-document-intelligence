import chromadb
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to ChromaDB
client = chromadb.PersistentClient(path="rag/vectorstore")

# Try to get collection safely
try:
    collection = client.get_collection("uae_documents")
except Exception as e:
    print(f"ChromaDB error: {e}")
    collection = None

# Connect to Gemini
gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def rag_agent(question: str) -> dict:
    
    if collection is None:
        return {
            "agent": "RAG Agent",
            "question": question,
            "answer": "Document database not available. Please contact administrator.",
            "pages": [],
            "source": "Error"
        }
    
    # Step 1: Search ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    # Step 2: Get pages
    pages = [m['page'] for m in results['metadatas'][0]]
    
    # Step 3: Combine content
    context = "\n\n".join(results['documents'][0])
    
    # Step 4: Send to Gemini
    prompt = f"""You are a UAE Labour Law expert.
Answer using only the content below.
Use bullet points.
Maximum 5 points.
Each point maximum 10 words.
Be direct and specific.

Content:
{context}

Question: {question}"""

    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return {
        "agent": "RAG Agent",
        "question": question,
        "answer": response.text,
        "pages": pages,
        "source": "UAE Labour Law PDF"
    }

if __name__ == "__main__":
    result = rag_agent("How many days annual leave?")
    print(f"\nAnswer:\n{result['answer']}")






# import chromadb
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = chromadb.PersistentClient(path="rag/vectorstore")
# collection = client.get_collection("uae_documents")

# def rag_agent(question: str) -> dict:
    
#     print(f"RAG Agent working on: {question}")
    
#     # Step 1: Search ChromaDB
#     results = collection.query(
#         query_texts=[question],
#         n_results=5
#     )
    
#     # Step 2: Get pages
#     pages = [m['page'] for m in results['metadatas'][0]]
    
#     # Step 3: Combine content
#     context = "\n\n".join(results['documents'][0])
    
#     # Step 4: Send to Ollama
#     prompt = f"""You are a UAE Labour Law expert.
# Answer using only the content below.
# Use bullet points.
# Maximum 5 points.
# Each point maximum 10 words.
# Be direct and specific.

# Content:
# {context}

# Question: {question}"""

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3.2:1b",
#             "prompt": prompt,
#             "stream": False
#         }
#     )
    
#     return {
#         "agent": "RAG Agent",
#         "question": question,
#         "answer": response.json()['response'],
#         "pages": pages,
#         "source": "UAE Labour Law PDF"
#     }

# if __name__ == "__main__":
#     result = rag_agent("How many days annual leave?")
#     print(f"\nAnswer:\n{result['answer']}")