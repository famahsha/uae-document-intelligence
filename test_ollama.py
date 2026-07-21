import requests

# Send a simple question to Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:1b",
        "prompt": "Say hello in one sentence",
        "stream": False
    }
)

# Print the answer
print("Ollama says:", response.json()["response"])