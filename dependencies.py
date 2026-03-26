from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore
from services.llm_service_gemini import LLMService
from config import settings
from services.chunking_service import ChunkingService


doc_processor = DocumentProcessor()
chunking_service = ChunkingService()  # Default chunk size and overlap can be adjusted as needed

vector_store = VectorStore(
    settings.QDRANT_HOST,
    settings.QDRANT_PORT,
    "documents",
    settings.EMBEDDING_MODEL
)

# llm = LLMService(
#     settings.VLLM_BASE_URL,
#     settings.MODEL_NAME
# )

llm = LLMService(model="gemini-2.5-flash")