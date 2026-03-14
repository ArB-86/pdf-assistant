```markdown
#  Intelligent PDF Assistant

> Ask questions about your PDF documents in plain language. Get accurate answers with source references — powered by RAG (Retrieval Augmented Generation).

---

##  What It Does

Searching information inside large PDFs (books, research papers, manuals, notes) is slow and painful. Generic AI chatbots like ChatGPT give general answers not based on *your* documents.

This project solves that — upload any PDF, ask a question, get an answer with exact source citations from your document.

---

## System Architecture

```
User Question
     │
     ▼
┌─────────────────┐
│  Streamlit UI   │  ← Upload PDFs, ask questions, view answers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PDF Processor  │  ← Extract text (PyPDF2), split into chunks
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Embedding & Search Module  │  ← Sentence Transformer (all-MiniLM-L6-v2)
│                             │    encodes chunks into 384-dim vectors
│                             │    Cosine similarity (sklearn) finds top-K
└────────────────┬────────────┘
                 │
                 ▼
┌─────────────────────────────┐
│   Answer Generation (LLM)   │  ← Groq (Llama 3.1 8B) via API
│                             │    answers from retrieved context only
└─────────────────────────────┘
```

---

##  Technology Stack

| Layer               | Technology                                                                 |
|---------------------|----------------------------------------------------------------------------|
| Language            | Python 3.10                                                                |
| UI Framework        | Streamlit                                                                  |
| PDF Parsing         | PyPDF2                                                                     |
| ML Embeddings       | Sentence Transformers (`all-MiniLM-L6-v2`)                                 |
| Vector Search       | scikit-learn (Cosine Similarity) + NumPy                                   |
| LLM / AI            | Groq Cloud (Llama 3.1 8B Instant)                                          |
| Environment         | python-dotenv                                                              |
| Containerization    | Docker                                                                     |

---

##  Getting Started

### Option 1: Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/pdf-assistant.git
cd pdf-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**  
Create a `.env` file in the root directory and add your [Groq API key](https://console.groq.com/keys):
```bash
GROQ_API_KEY=your_api_key_here
```
> You can get a free API key by signing up at [groq.com](https://groq.com).

**4. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

### Option 2: Run with Docker

```bash
# Build the image
docker build -t pdf-assistant .

# Run the container (replace with your actual key)
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here pdf-assistant
```

---

## ✨ Features

- **Multiple PDF upload** — process several documents simultaneously
- **Semantic search** — understands meaning, not just keywords
- **Source citations** — every answer shows which file and page it came from
- **Chat history** — follow-up questions use previous context
- **Relevance scores** — shows how confident the retrieval is
- **Clean dark UI** — professional interface built with Streamlit
- **Fast inference** — powered by Groq's ultra‑fast LPU inference engine

---

## 🧠 How RAG Works (Technical)

**1. Indexing Phase (when PDFs are uploaded)**
```
PDF → Extract Text → Split into 300-word chunks (50-word overlap)
    → Encode each chunk using Sentence Transformer → Store vectors
```

**2. Retrieval Phase (when question is asked)**
```
Question → Encode with same model → Compute cosine similarity vs all chunks
         → Return top‑3 most semantically similar chunks
```

**3. Generation Phase**
```
Top‑3 chunks + Question → Groq (Llama 3.1 8B) → Answer with source references
```

The key insight: by using dense vector embeddings instead of keyword search, the system finds *semantically* related content even when exact words don't match.

---

##  Project Structure

```
pdf-assistant/
├── app.py              # Main Streamlit application & UI
├── pdf_processor.py    # PDF text extraction & chunking
├── vector_search.py    # Sentence Transformer encoding & cosine search
├── qa_engine.py        # Groq API integration & prompt engineering
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── .env.example        # Environment variable template
└── README.md
```

---

## Future Scope

- Support for Word (.docx) and plain text files
- Vector database (ChromaDB/FAISS) for large document collections
- Multi‑language support
- User authentication system
- Export answers to PDF/Word
- Mobile‑responsive UI
- Switchable LLM backends (OpenAI, Gemini, etc.)

---

##  References

- [RAG Paper — Facebook AI Research](https://arxiv.org/abs/2005.11401)
- [Groq Cloud Documentation](https://console.groq.com/docs/)
- [Sentence Transformers](https://www.sbert.net)
- [Streamlit Documentation](https://docs.streamlit.io)

---

##  Author

ARYA BHAWSAR 
*3rd Year B.Tech CSE Student*

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
```
