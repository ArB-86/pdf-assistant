# Intelligent PDF Assistant

The Intelligent PDF Assistant is an AI based application that allows users to upload PDF documents and ask questions about their content in natural language. The system reads the uploaded PDFs, finds the most relevant information, and generates answers using a Retrieval Augmented Generation (RAG) approach.

Unlike traditional chatbots, the system does not rely on general knowledge. Instead, it retrieves information directly from the uploaded documents and provides answers along with the source file and page number.

---

## Objective

Searching for information inside large documents such as books, research papers, reports, or manuals can be time consuming. Users often need to read many pages to find a small piece of information.

The objective of this project is to build an intelligent assistant that can:

- Upload and process multiple PDF documents
- Understand user questions written in natural language
- Retrieve the most relevant information from the documents
- Generate accurate answers based on document content
- Provide source references such as file name and page number

---

## Technology Stack

Programming Language  
Python

User Interface  
Streamlit

PDF Processing  
PyPDF2

Embedding Model  
Sentence Transformers (all-MiniLM-L6-v2)

Vector Similarity Search  
Scikit Learn Cosine Similarity

Numerical Computation  
NumPy

Large Language Model  
Groq API using Llama 3.1

Environment Management  
Python Dotenv

---

## How the System Works

The system follows a Retrieval Augmented Generation pipeline.

### 1. Document Processing
Users upload one or more PDF files. The system extracts text from each page of the documents.

### 2. Text Chunking
The extracted text is divided into smaller chunks of approximately 300 words with a small overlap to preserve context.

### 3. Embedding Generation
Each text chunk is converted into a numerical vector representation using the Sentence Transformer model.

### 4. Vector Index Creation
All chunk vectors are stored in memory to create a searchable semantic index.

### 5. Question Processing
When a user asks a question, the question is also converted into an embedding vector.

### 6. Semantic Retrieval
Cosine similarity is used to compare the question vector with all document vectors. The most relevant chunks are retrieved.

### 7. Answer Generation
The retrieved chunks and the user question are sent to the language model. The model generates the final answer based only on the provided document context.

---

## Project Structure

app.py  
Main Streamlit application that handles the user interface, file uploads, question input, and overall pipeline.

pdf_processor.py  
Extracts text from PDF files and splits the text into smaller chunks.

vector_search.py  
Creates embeddings for text chunks and performs semantic similarity search.

qa_engine.py  
Handles the interaction with the language model and generates answers.

requirements.txt  
Contains all required Python dependencies for the project.

Dockerfile  
Used for containerizing the application.

README.md  
Documentation for the project.

---

## Key Features

- Upload multiple PDF documents
- Ask questions in natural language
- Semantic search using embeddings
- Answers generated from document content
- Source citation with file name and page number
- Interactive question answering interface
- Relevance score for retrieved text chunks

---

## Installation and Setup

### Step 1 Clone the repository

```
git clone https://github.com/yourusername/pdf-assistant.git
cd pdf-assistant
```

### Step 2 Install dependencies

```
pip install -r requirements.txt
```

### Step 3 Add API key

Create a file named `.env` and add your API key:

```
GROQ_API_KEY=your_api_key_here
```

### Step 4 Run the application

```
streamlit run app.py
```

### Step 5 Open the application in your browser

```
http://localhost:8501
```

---

## Future Improvements

- Support for additional document formats such as Word and text files
- Integration with vector databases such as FAISS or ChromaDB
- Support for larger document collections
- User authentication system
- Export answers to PDF or text format
- Multi language document support

---

## References

RAG Paper  
https://arxiv.org/abs/2005.11401

Sentence Transformers  
https://www.sbert.net

Streamlit Documentation  
https://docs.streamlit.io

Groq API Documentation  
https://console.groq.com/docs
