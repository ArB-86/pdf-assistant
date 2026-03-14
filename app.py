import streamlit as st
import time
import os
from dotenv import load_dotenv
from pdf_processor import extract_text_from_pdfs, split_into_chunks
from vector_search import build_index, find_relevant_chunks
from qa_engine import get_answer, configure_gemini

# Load API key from .env automatically
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    configure_gemini(api_key)

st.set_page_config(page_title="PDF Assistant", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
    .stApp { background: #0d0f14; color: #e2e8f0; }
    section[data-testid="stSidebar"] { background: #111318 !important; border-right: 1px solid #1e2330; }
    .stTextInput > div > div > input { background: #161b27 !important; border: 1px solid #2d3748 !important; color: #e2e8f0 !important; border-radius: 8px !important; }
    .stTextInput > div > div > input:focus { border-color: #4f8ef7 !important; box-shadow: 0 0 0 2px rgba(79,142,247,0.15) !important; }
    .stButton > button { background: #4f8ef7 !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; padding: 0.5rem 1.5rem !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { background: #3b7de8 !important; transform: translateY(-1px) !important; box-shadow: 0 4px 15px rgba(79,142,247,0.3) !important; }
    .stFileUploader { background: #161b27 !important; border: 2px dashed #2d3748 !important; border-radius: 12px !important; padding: 1rem !important; }
    .chat-message { padding: 1rem 1.2rem; border-radius: 12px; margin: 0.5rem 0; line-height: 1.6; font-size: 0.95rem; }
    .chat-user { background: #1a2035; border-left: 3px solid #4f8ef7; color: #e2e8f0; }
    .chat-assistant { background: #141a28; border-left: 3px solid #34d399; color: #e2e8f0; }
    .chat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem; font-family: 'IBM Plex Mono', monospace; }
    .label-user { color: #4f8ef7; }
    .label-assistant { color: #34d399; }
    .source-card { background: #161b27; border: 1px solid #2d3748; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.3rem 0; font-size: 0.85rem; color: #94a3b8; font-family: 'IBM Plex Mono', monospace; }
    .stat-badge { display: inline-block; background: #1a2035; border: 1px solid #2d3748; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-family: 'IBM Plex Mono', monospace; color: #94a3b8; margin: 0.2rem; }
    .app-title { font-family: 'IBM Plex Mono', monospace; font-size: 1.8rem; font-weight: 600; color: #e2e8f0; }
    .app-subtitle { font-size: 0.85rem; color: #64748b; font-family: 'IBM Plex Mono', monospace; }
    hr { border-color: #1e2330 !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session State
for key, val in [("chunks",[]),("vectors",None),("chat_history",[]),("pdfs_processed",False),("processed_filenames",[])]:
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar
with st.sidebar:
    st.markdown('<p class="app-title">📄 PDF<br>Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">// intelligent document Q&A</p>', unsafe_allow_html=True)
    st.markdown("---")

    if api_key:
        st.markdown('<p style="color:#34d399;font-size:0.82rem;font-family:IBM Plex Mono,monospace;">✅ API key loaded from .env</p>', unsafe_allow_html=True)
    else:
        st.error("❌ No API key. Add GEMINI_API_KEY to .env file.")

    st.markdown("---")
    st.markdown("**📂 Upload PDFs**")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        new_names = sorted([f.name for f in uploaded_files])
        if new_names != st.session_state.processed_filenames:
            if st.button("⚡ Process Documents"):
                progress = st.progress(0)
                with st.spinner("Reading PDFs..."):
                    documents = extract_text_from_pdfs(uploaded_files)
                progress.progress(33)
                with st.spinner("Splitting into chunks..."):
                    chunks = split_into_chunks(documents)
                progress.progress(66)
                with st.spinner("Building semantic index..."):
                    vectors = build_index(chunks)
                progress.progress(100)
                time.sleep(0.3)
                progress.empty()
                st.session_state.chunks = chunks
                st.session_state.vectors = vectors
                st.session_state.pdfs_processed = True
                st.session_state.chat_history = []
                st.session_state.processed_filenames = new_names
                st.rerun()

    if st.session_state.pdfs_processed:
        st.markdown("---")
        st.markdown("**📊 Index Stats**")
        st.markdown(f'<span class="stat-badge">📄 {len(st.session_state.processed_filenames)} file(s)</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="stat-badge">🧩 {len(st.session_state.chunks)} chunks</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="stat-badge">💬 {len(st.session_state.chat_history)} messages</span>', unsafe_allow_html=True)
        for name in st.session_state.processed_filenames:
            st.markdown(f'<div class="source-card">✓ {name}</div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")
    st.markdown('<p style="font-size:0.72rem;color:#374151;font-family:IBM Plex Mono,monospace;">Built with Python · Streamlit<br>Sentence Transformers · Gemini</p>', unsafe_allow_html=True)

# Main Area
if not api_key:
    st.error("No Gemini API key found. Add `GEMINI_API_KEY=your_key` to your `.env` file and restart.")

elif not st.session_state.pdfs_processed:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;padding:3rem 2rem;background:#111318;border-radius:16px;border:1px solid #1e2330;">
            <div style="font-size:3rem;">📄</div>
            <h2 style="font-family:'IBM Plex Mono',monospace;color:#e2e8f0;margin:1rem 0 0.5rem;">PDF Assistant</h2>
            <p style="color:#64748b;font-size:0.9rem;">Ask questions. Get answers. With sources.</p>
            <br>
            <div style="text-align:left;background:#161b27;border-radius:10px;padding:1.2rem;margin-top:1rem;">
                <p style="color:#94a3b8;font-size:0.85rem;margin:0 0 0.8rem;font-family:'IBM Plex Mono',monospace;">// QUICK START</p>
                <p style="color:#34d399;font-size:0.85rem;margin:0.3rem 0;">✅ API key loaded</p>
                <p style="color:#e2e8f0;font-size:0.85rem;margin:0.3rem 0;">① Upload one or more PDF files in the sidebar</p>
                <p style="color:#e2e8f0;font-size:0.85rem;margin:0.3rem 0;">② Click "Process Documents"</p>
                <p style="color:#e2e8f0;font-size:0.85rem;margin:0.3rem 0;">③ Ask anything about your documents below</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown('<p class="app-subtitle" style="margin-bottom:1rem;">// Ask anything about your uploaded documents</p>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:2rem;color:#374151;">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:0.9rem;">
                ✅ Documents indexed and ready.<br>Ask your first question below ↓
            </p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message chat-user"><div class="chat-label label-user">YOU</div>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message chat-assistant"><div class="chat-label label-assistant">ASSISTANT</div>{msg["content"]}</div>', unsafe_allow_html=True)
            if msg.get("sources"):
                with st.expander(f"📚 View {len(msg['sources'])} source(s) used"):
                    for i, src in enumerate(msg["sources"]):
                        score_color = "#34d399" if src["score"] > 0.5 else "#f59e0b" if src["score"] > 0.3 else "#94a3b8"
                        st.markdown(f'<div class="source-card"><span style="color:{score_color}">●</span> <strong>Source {i+1}</strong> — {src["source"]} | Page {src["page"]} | Relevance: <span style="color:{score_color}">{src["score"]}</span></div><div style="background:#0d0f14;border-radius:6px;padding:0.6rem;margin:0.3rem 0;font-size:0.8rem;color:#64748b;font-family:IBM Plex Mono,monospace;">{src["text"][:300]}{"..." if len(src["text"]) > 300 else ""}</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([5,1])
    with col1:
        question = st.text_input("Ask", placeholder="e.g. What is the main objective of this project?", label_visibility="collapsed", key="question_input")
    with col2:
        ask_btn = st.button("Ask →", use_container_width=True)

    if ask_btn and question.strip():
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.spinner("Searching documents..."):
            relevant = find_relevant_chunks(question, st.session_state.chunks, st.session_state.vectors, top_k=3)
        with st.spinner("Generating answer..."):
            answer = get_answer(question, relevant, chat_history=st.session_state.chat_history[:-1])
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "sources": relevant})
        st.rerun()