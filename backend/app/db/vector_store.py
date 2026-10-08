from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings


def get_vector_store() -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GEMINI_API_KEY,
    )
    return Chroma(
        collection_name="rag_gemini",  # new name avoids old-dimension conflicts
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )