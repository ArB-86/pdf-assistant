import PyPDF2
import re


def extract_text_from_pdfs(pdf_files):
    """
    Extract text from one or more PDF files.
    Returns a list of dicts with filename and text content.
    """
    documents = []

    for pdf_file in pdf_files:
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            full_text = ""
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # Clean up whitespace
                    text = re.sub(r'\s+', ' ', text).strip()
                    full_text += f"\n[Page {page_num + 1}]\n{text}\n"

            documents.append({
                "filename": getattr(pdf_file, "name", "document.pdf"),
                "text": full_text,
                "pages": len(reader.pages)
            })
        except Exception as e:
            documents.append({
                "filename": getattr(pdf_file, "name", "document.pdf"),
                "text": "",
                "pages": 0,
                "error": str(e)
            })

    return documents


def split_into_chunks(documents, chunk_size=300, overlap=50):
    """
    Split document text into overlapping chunks for better retrieval.
    Each chunk stores the source filename for citation purposes.
    """
    all_chunks = []

    for doc in documents:
        if not doc.get("text"):
            continue

        words = doc["text"].split()
        filename = doc["filename"]
        i = 0

        while i < len(words):
            chunk_words = words[i: i + chunk_size]
            chunk_text = " ".join(chunk_words)

            # Try to detect which page this chunk is from
            page_match = re.search(r'\[Page (\d+)\]', chunk_text)
            page_num = page_match.group(1) if page_match else "?"

            all_chunks.append({
                "text": chunk_text,
                "source": filename,
                "page": page_num,
                "chunk_id": len(all_chunks)
            })

            i += chunk_size - overlap  # overlapping chunks

    return all_chunks