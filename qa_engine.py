import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

def configure_gemini(api_key=None):
    # kept same name so app.py doesn't need changes
    global _client
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found in .env file.")
    _client = Groq(api_key=key)

def get_client():
    global _client
    if _client is None:
        configure_gemini()
    return _client

def get_answer(question, relevant_chunks, chat_history=None):
    context_parts = []
    for i, chunk in enumerate(relevant_chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['source']}, Page {chunk['page']}]\n{chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    history_str = ""
    if chat_history:
        history_str = "\n\nPrevious conversation:\n"
        for msg in chat_history[-4:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_str += f"{role}: {msg['content']}\n"

    prompt = f"""You are an intelligent PDF assistant. Answer using ONLY the context below.

RULES:
1. Answer ONLY from the provided context. Do not use outside knowledge.
2. If the answer is not in the context, say: "I could not find this in the uploaded documents."
3. Always mention which source/page your answer comes from.
4. Be clear and concise.

Document Context:
{context}
{history_str}

Question: {question}

Answer (with source references):"""

    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content