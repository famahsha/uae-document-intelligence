# from google import genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# def supervisor_agent(question: str) -> str:
    
#     print(f"Supervisor deciding for: {question}")
    
#     # Ask Gemini to decide which agent to use
#     prompt = f"""You are a supervisor deciding which agent to use.

# You have two agents:
# 1. RAG Agent - answers questions about UAE Labour Law document
# 2. Search Agent - searches internet for current information

# Question: {question}

# Reply with ONLY one word:
# - "RAG" if question is about UAE Labour law, employment, leave, salary, contracts
# - "SEARCH" if question needs current information like prices, news, rates"""

#     response = gemini.models.generate_content(
#         model="gemini-2.0-flash-lite",
#         contents=prompt
#     )
    
#     decision = response.text.strip().upper()
    
#     # Make sure decision is valid
#     if "RAG" in decision:
#         return "RAG"
#     else:
#         return "SEARCH"

# # Test
# if __name__ == "__main__":
#     questions = [
#         "How many days annual leave?",
#         "What is gold price today?",
#         "What is end of service gratuity?",
#         "What is UAE population 2024?"
#     ]
    
#     for q in questions:
#         decision = supervisor_agent(q)
#         print(f"Q: {q}")
#         print(f"Decision: {decision}\n")








import requests
import os
from dotenv import load_dotenv

load_dotenv()

def supervisor_agent(question: str) -> str:
    
    prompt = f"""You are a supervisor deciding which agent to use.

Two agents available:
1. RAG - for UAE Labour Law questions about employment, leave, salary, contracts, gratuity
2. SEARCH - for current information like prices, news, rates, today's data

Question: {question}

Reply with ONLY one word: RAG or SEARCH"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )
    
    answer = response.json()['response'].strip().upper()
    
    if "RAG" in answer:
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