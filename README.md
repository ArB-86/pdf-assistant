# Intelligent PDF Assistant

> Ask questions about your PDF documents in plain language and get accurate answers with source references — powered by Retrieval Augmented Generation (RAG).

---

## What It Does

Searching information inside large PDFs (books, research papers, manuals, notes) is slow and inefficient. Generic AI chatbots often provide general answers that are not based on *your* documents.

This project solves that problem. Upload any PDF, ask a question, and receive an answer with exact source citations from the document.

---

## Technology Stack

| Layer            | Technology                                 |
| ---------------- | ------------------------------------------ |
| Language         | Python 3.10                                |
| UI Framework     | Streamlit                                  |
| PDF Parsing      | PyPDF2                                     |
| ML Embeddings    | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Search    | scikit-learn (Cosine Similarity) + NumPy   |
| LLM / AI         | Groq Cloud (Llama 3.1 8B Instant)          |
| Environment      | python-dotenv                              |
| Containerization | Docker                                     |

---

## Getting Started

### Run Locally

**1. Clone the repository**

```
git clone https://github.com/YOUR_USERNAME/pdf-assistant.git
cd pdf-assistant
```

**2. Install dependencies**

```
pip install -r requirements.txt
```

**3. Configure API key**

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

You can obtain a free API key from Groq Cloud.

**4. Run the application**

```
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

### Run with Docker

Build the container:

```
docker build -t pdf-assistant .
```

Run the container:

```
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here pdf-assistant
```

---

## Features

* Upload and analyze multiple PDFs
* Semantic search using vector embeddings
* Answers with exact source citations
* Chat-style question answering
* Relevance scoring for retrieved content
* Clean interactive UI built with Streamlit
* Fast responses using Groq inference

---

## How It Works

1. **PDF Processing**

   * Text is extracted from uploaded PDFs.
   * Content is split into overlapping chunks for better context.

2. **Embedding Generation**

   * Each chunk is converted into a vector embedding using a Sentence Transformer model.

3. **Semantic Retrieval**

   * User questions are converted into embeddings.
   * Cosine similarity finds the most relevant document chunks.

4. **Answer Gener**
