from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore
from services.llm_service import LLMService
from config import settings


doc_processor = DocumentProcessor()

vector_store = VectorStore(
    settings.QDRANT_HOST,
    settings.QDRANT_PORT,
    "documents",
    settings.EMBEDDING_MODEL
)

llm = LLMService(
    settings.VLLM_BASE_URL,
    settings.MODEL_NAME
)