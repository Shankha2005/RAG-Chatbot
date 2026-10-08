import json
from typing import Generator

from google import genai
from google.genai import types

from app.db.vector_store import get_vector_store
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Verify this name against your key (see the snippet below)
CHAT_MODEL = "gemini-2.5-flash"


def format_docs(docs):
    formatted = []
    for doc in docs:
        page = doc.metadata.get("page")
        page_label = page + 1 if isinstance(page, int) else "Unknown"
        formatted.append(f"[Page {page_label}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)


def stream_gemini_api(system_instruction: str, user_query: str) -> Generator[str, None, None]:
    try:
        stream = client.models.generate_content_stream(
            model=CHAT_MODEL,
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,
            ),
        )
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n[System Error: Gemini API Connection Failed - {str(e)}]"


def answer_query_stream(query: str, chat_history: list = None, filter_doc_id: str = None) -> Generator[str, None, None]:
    vector_store = get_vector_store()

    try:
        total_docs = vector_store._collection.count()
    except Exception:
        total_docs = 5

    if total_docs == 0:
        yield json.dumps({"type": "chunk", "content": "Please upload a document first!"}) + "\n"
        return

    search_kwargs = {
        "k": min(5, total_docs),
        "fetch_k": min(20, total_docs),
        "lambda_mult": 0.7,
    }
    if filter_doc_id:
        search_kwargs["filter"] = {"document_id": filter_doc_id}

    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs=search_kwargs)
    docs = retriever.invoke(query)

    sources = [
        {
            "page": (doc.metadata.get("page") + 1) if isinstance(doc.metadata.get("page"), int) else "Unknown",
            "source": doc.metadata.get("source", "Unknown"),
            "content_snippet": doc.page_content[:150] + "...",
        }
        for doc in docs
    ]
    yield json.dumps({"type": "citations", "citations": sources}) + "\n"

    context_str = format_docs(docs)
    system_prompt = (
        "You are an expert, helpful AI assistant.\n"
        "Your task is to answer the user's question based strictly on the provided context.\n\n"
        "<instructions>\n"
        "1. Use ONLY the provided context to answer the question.\n"
        "2. If the context does not contain the answer, strictly reply: 'I don't have enough information to answer that based on the provided documents.'\n"
        "3. Do NOT hallucinate or use outside knowledge.\n"
        "4. Whenever you state a fact, append the page number from the context using the format [Page X] immediately after the claim.\n"
        "</instructions>\n\n"
        f"<context>\n{context_str}\n</context>"
    )

    for chunk in stream_gemini_api(system_instruction=system_prompt, user_query=query):
        yield json.dumps({"type": "chunk", "content": chunk}) + "\n"