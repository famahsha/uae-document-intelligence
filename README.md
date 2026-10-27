# UAE Document Intelligence Platform

A multi-agent RAG system that answers questions about UAE Labour Law documents and falls back to live web search when the documents don't have the answer.

**Live demo:** https://uae-document-intelligence-n3e9u4wtxjynk7uuhm3qzr.streamlit.app

## What it does
- Answers questions over UAE Labour Law documents, with answers grounded in the retrieved text.
- Routes each question to the right agent: document Q&A or real-time web search.
- Pauses for human approval on high-risk queries before answering.
- Lets you upload your own documents in the app and ask questions about them.
- Exposes document search as an MCP tool, so any MCP-compatible AI client can discover and call it.

## Architecture
Three agents orchestrated with LangGraph, using conditional edges and stateful workflow control:

| Agent | Role |
|---|---|
| Supervisor | Classifies the query and routes it |
| RAG agent | Retrieves from ChromaDB and answers with Google Gemini |
| Search agent | Real-time web search through the Tavily API |

A human-in-the-loop approval step sits in front of high-risk queries.

```
User query -> Supervisor -> RAG agent (ChromaDB + Gemini)
                         -> Search agent (Tavily)
                         -> Human approval (high-risk)
```

## Tech stack
Python, LangChain, LangGraph, ChromaDB, Google Gemini API, Tavily API, MCP, Streamlit, Git/GitHub

## Run locally
```bash
git clone https://github.com/famahsha/uae-document-intelligence
cd uae-document-intelligence
pip install -r requirements.txt
# set GOOGLE_API_KEY and TAVILY_API_KEY in your environment or .env
streamlit run app.py
```
<!-- Check the entry file name and env variable names match your repo. -->

## Challenges solved
- Vector database persistence on Streamlit Cloud.
- API rate limits on the cloud deployment.

## Limitations
This is a learning project. It is not legal advice, and answers should be checked against the official source.

## Author
Fathimath Mahshana, Abu Dhabi. [LinkedIn](https://linkedin.com/in/fathimath-mahshana)
