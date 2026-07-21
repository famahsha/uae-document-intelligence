from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def supervisor_agent(question: str) -> str:
    
    print(f"Supervisor deciding for: {question}")
    
    prompt = f"""You are a supervisor deciding which agent to use.

Two agents available:
1. RAG Agent - for UAE Labour Law questions about employment, leave, salary, contracts, gratuity
2. Search Agent - for current information like prices, news, rates, today's data

Question: {question}

Reply with ONLY one word: RAG or SEARCH"""

    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    decision = response.text.strip().upper()
    
    if "RAG" in decision:
        return "RAG"
    else:
        return "SEARCH"

if __name__ == "__main__":
    questions = [
        "How many days annual leave?",
        "What is gold price today?",
    ]
    for q in questions:
        print(f"Q: {q} → {supervisor_agent(q)}")



# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def supervisor_agent(question: str) -> str:
    
#     prompt = f"""You are a supervisor deciding which agent to use.

# Two agents available:
# 1. RAG - for UAE Labour Law questions about employment, leave, salary, contracts, gratuity
# 2. SEARCH - for current information like prices, news, rates, today's data

# Question: {question}

# Reply with ONLY one word: RAG or SEARCH"""

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3.2:1b",
#             "prompt": prompt,
#             "stream": False
#         }
#     )
    
#     answer = response.json()['response'].strip().upper()
    
#     if "RAG" in answer:
#         return "RAG"
#     else:
#         return "SEARCH"

# if __name__ == "__main__":
#     questions = [
#         "How many days annual leave?",
#         "What is gold price today?",
#     ]
#     for q in questions:
#         print(f"Q: {q} → {supervisor_agent(q)}")