import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Production RAG API"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    class Config:
        env_file = ".env"

settings = Settings()