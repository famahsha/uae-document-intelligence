from agents.supervisor_agent import supervisor_agent
from agents.rag_agent import rag_agent
from agents.search_agent import search_agent
from hitl import human_review

def ask(question: str) -> dict:
    
    print(f"\nQuestion: {question}")
    print("-" * 40)
    
    # Step 1: Supervisor decides
    decision = supervisor_agent(question)
    
    # Step 2: Run correct agent
    if decision == "RAG":
        result = rag_agent(question)
    else:
        result = search_agent(question)
    
    # Step 3: Human reviews
    result = human_review(result)
    
    # Step 4: Show final answer
    print(f"\nFinal Answer:\n{result['answer']}")
    print(f"Status: {result['status']}")
    
    return result

# Test
if __name__ == "__main__":
    ask("How many days annual leave?")