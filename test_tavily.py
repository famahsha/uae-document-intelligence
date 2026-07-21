from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# More specific search
result = client.search(
    "UAE Labour Law annual leave days 2024",
    search_depth="basic",
    max_results=3
)

# Print results clearly
for i, r in enumerate(result['results']):
    print(f"\nResult {i+1}:")
    print(r['title'])
    print(r['content'][:200])