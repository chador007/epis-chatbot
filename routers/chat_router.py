from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from dependencies import doc_processor, vector_store, llm
from models.schemas import QueryRequest, QueryResponse, SearchResultSchema

from services.chunking_service import ChunkingService

router = APIRouter()

UPLOAD_DIR = Path("./documents")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = doc_processor.extract_text(str(file_path))
    cleaned_text = doc_processor.clean_text(text)

    chunks = ChunkingService().chunk(cleaned_text)

    n = vector_store.add(chunks, {"document_name": file.filename})

    return {"chunks": n}


@router.post("/chat", response_model=QueryResponse)
async def query(req: QueryRequest):

    hits = vector_store.search(req.question, req.top_k)

    context = [h.text for h in hits]  # ✅ dataclass attribute

    answer = llm.generate(req.question, context)

    return QueryResponse(
        answer=answer,
        sources=[
            SearchResultSchema(
                text=h.text,
                score=h.score,
                chunk_id=h.chunk_id,
                document_name=h.document_name
            )
            for h in hits
        ]
    )