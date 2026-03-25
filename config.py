import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    raw_port = os.getenv("QDRANT_PORT")
    QDRANT_PORT = int(raw_port) if raw_port else None
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    VLLM_BASE_URL = os.getenv("VLLM_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()