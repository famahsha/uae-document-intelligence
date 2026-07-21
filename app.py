import streamlit as st
from agents.supervisor_agent import supervisor_agent
from agents.rag_agent import rag_agent
from agents.search_agent import search_agent
import fitz
import chromadb
import os

# Page setup
st.set_page_config(
    page_title="UAE Document Intelligence",
    page_icon="🇦🇪",
    layout="wide"
)

# Title
st.title("🇦🇪 UAE Document Intelligence Platform")

# Initialize session state for pending answers
if 'pending_answers' not in st.session_state:
    st.session_state['pending_answers'] = []

# Sidebar
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
                
                # Supervisor decides
                decision = supervisor_agent(question)
                
                # Run correct agent
                if decision == "RAG":
                    result = rag_agent(question)
                    source = "📄 UAE Labour Law Document"
                else:
                    result = search_agent(question)
                    source = "🌐 Internet Search"
                
                # Add to pending answers for manager
                st.session_state['pending_answers'].append({
                    "question": question,
                    "answer": result['answer'],
                    "agent": result['agent'],
                    "source": source,
                    "status": "Pending"
                })
                
                # Show user that answer is being reviewed
                st.info(f"Source: {source}")
                st.success("✅ Your question has been answered!")
                st.markdown(result['answer'])
                st.warning("⏳ This answer is pending manager approval")
        else:
            st.warning("Please type a question first")

# ═══════════════════════════════════
# PAGE 2 — UPLOAD DOCUMENT
# ═══════════════════════════════════
elif page == "📄 Upload Document":
    
    st.header("📄 Upload Document")
    st.write("Upload a PDF to add to the knowledge base")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf']
    )
    
    if uploaded_file:
        if st.button("Process Document", type="primary"):
            with st.spinner("Reading and storing document..."):
                
                # Save file
                save_path = f"rag/documents/{uploaded_file.name}"
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Read PDF
                doc = fitz.open(save_path)
                pages = []
                for i, page in enumerate(doc):
                    text = page.get_text()
                    if text.strip():
                        pages.append({
                            "id": f"{uploaded_file.name}_page_{i+1}",
                            "text": text,
                            "page": i+1
                        })
                
                # Store in ChromaDB
                client = chromadb.PersistentClient(
                    path="rag/vectorstore"
                )
                try:
                    collection = client.get_collection("uae_documents")
                except:
                    collection = client.create_collection("uae_documents")
                
                collection.add(
                    documents=[p["text"] for p in pages],
                    ids=[p["id"] for p in pages],
                    metadatas=[{"page": p["page"]} for p in pages]
                )
                
                st.success(f"✅ Document processed!")
                st.info(f"Added {len(pages)} pages to knowledge base")

# ═══════════════════════════════════
# PAGE 3 — MANAGER REVIEW
# ═══════════════════════════════════
elif page == "👨‍💼 Manager Review":
    
    st.header("👨‍💼 Manager Review Panel")
    st.write("Review and approve AI generated answers")
    
    pending = st.session_state['pending_answers']
    
    if not pending:
        st.info("No answers pending review")
    else:
        st.write(f"**{len(pending)} answer(s) waiting for review:**")
        
        for i, item in enumerate(pending):
            with st.expander(f"Question {i+1}: {item['question']}"):
                st.write(f"**Source:** {item['source']}")
                st.write(f"**Agent:** {item['agent']}")
                st.write(f"**Answer:**")
                st.markdown(item['answer'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{i}"):
                        st.session_state['pending_answers'][i]['status'] = "Approved ✅"
                        st.success("Approved!")
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{i}"):
                        st.session_state['pending_answers'][i]['status'] = "Rejected ❌"
                        st.error("Rejected!")
                        st.rerun()
                
                st.write(f"**Status:** {item['status']}")