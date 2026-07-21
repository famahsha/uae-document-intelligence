from tavily import TavilyClient
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def search_agent(question: str) -> dict:
    
    print(f"Search Agent working on: {question}")
    
    # Step 1: Search internet
    results = tavily.search(
        question,
        search_depth="basic",
        max_results=3
    )
    
    # Step 2: Combine results
    context = "\n\n".join([
        r['content'] for r in results['results']
    ])
    
    # Step 3: Send to Gemini for clean answer
    prompt = f"""Answer this question in simple bullet points.
Maximum 5 bullet points.
Each bullet point maximum 10 words.
Be direct and clear.

Information:
{context}

Question: {question}"""

    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return {
        "agent": "Search Agent",
        "question": question,
        "answer": response.text,
        "source": "Internet Search"
    }

if __name__ == "__main__":
    result = search_agent("What is UAE minimum wage 2024?")
    print(f"\nAnswer:\n{result['answer']}")










# from tavily import TavilyClient
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# def search_agent(question: str) -> dict:
    
#     print(f"Search Agent working on: {question}")
    
#     # Search internet
#     results = tavily.search(
#         question,
#         search_depth="basic",
#         max_results=3
#     )
    
#     context = "\n\n".join([
#         r['content'] for r in results['results']
#     ])
    
#     # Send to Ollama
#     prompt = f"""Answer in simple bullet points.
# Maximum 5 points.
# Each point maximum 10 words.
# Be direct and clear.

# Information:
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
#         "agent": "Search Agent",
#         "question": question,
#         "answer": response.json()['response'],
#         "source": "Internet Search"
#     }

# if __name__ == "__main__":
#     result = search_agent("What is UAE minimum wage 2024?")
#     print(f"\nAnswer:\n{result['answer']}")