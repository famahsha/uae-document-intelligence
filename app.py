import streamlit as st
from agents.supervisor_agent import supervisor_agent
from agents.rag_agent import rag_agent
from agents.search_agent import search_agent
import fitz
import chromadb
import os

# ═══════════════════════════════════
# AUTO-SETUP CHROMADB IF EMPTY
# ═══════════════════════════════════
def setup_chromadb_if_needed():
    client = chromadb.PersistentClient(path="rag/vectorstore")
    try:
        collection = client.get_collection("uae_documents")
        if collection.count() > 0:
            return  # already has data
    except:
        pass
    
    # Need to create it
    pdf_path = "rag/documents/uae_labour_law.pdf"
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        pages = []
        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append({
                    "id": f"page_{i+1}",
                    "text": text,
                    "page": i+1
                })
        
        try:
            client.delete_collection("uae_documents")
        except:
            pass
        
        collection = client.create_collection("uae_documents")
        collection.add(
            documents=[p["text"] for p in pages],
            ids=[p["id"] for p in pages],
            metadatas=[{"page": p["page"]} for p in pages]
        )

setup_chromadb_if_needed()

# ═══════════════════════════════════
# PAGE SETUP
# ═══════════════════════════════════
st.set_page_config(
    page_title="UAE Document Intelligence",
    page_icon="🇦🇪",
    layout="wide"
)

st.title("🇦🇪 UAE Document Intelligence Platform")

if 'pending_answers' not in st.session_state:
    st.session_state['pending_answers'] = []

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "💬 Ask Questions",
    "📄 Upload Document",
    "👨‍💼 Manager Review",
])

# ═══════════════════════════════════
# PAGE 1 — EMPLOYEE: ASK QUESTIONS
# ═══════════════════════════════════
if page == "💬 Ask Questions":
    
    st.header("💬 Ask a Question")
    st.write("Ask anything about UAE Labour Law or current information")
    
    question = st.text_input(
        "Type your question:",
        placeholder="Example: How many days annual leave?"
    )
    
    if st.button("Ask", type="primary"):
        if question:
            with st.spinner("Finding answer..."):
                
                decision = supervisor_agent(question)
                
                if decision == "RAG":
                    result = rag_agent(question)
                    source = "📄 UAE Labour Law Document"
                else:
                    result = search_agent(question)
                    source = "🌐 Internet Search"
                
                st.session_state['pending_answers'].append({
                    "question": question,
                    "answer": result['answer'],
                    "agent": result['agent'],
                    "source": source,
                    "status": "Pending"
                })
                
                st.info(f"Source: {source}")
                st.success("✅ Answer found!")
                st.markdown(result['answer'])
        else:
            st.warning("Please type a question first")

# ═══════════════════════════════════
# PAGE 2 — UPLOAD DOCUMENT
# ═══════════════════════════════════
elif page == "📄 Upload Document":
    
    st.header("📄 Upload Document")
    st.write("Upload a PDF to add to the