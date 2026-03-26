from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from networkx import hits

from dependencies import doc_processor,chunking_service, vector_store, llm
from models.schemas import QueryRequest, QueryResponse, SearchResultSchema

import logging
from datetime import datetime

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

    chunks = chunking_service.chunk(cleaned_text)

    n = vector_store.add(chunks, {"document_name": file.filename})

    return {"chunks": n}

chat_logger = logging.getLogger("chat_questions")
chat_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('chat_logs.txt')
formatter = logging.Formatter('%(asctime)s - User Question: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

chat_logger.addHandler(file_handler)
chat_logger.propagate = False

@router.post("/chat", response_model=QueryResponse)
async def query(req: QueryRequest):
  
    chat_logger.info(req.question)

    hits = vector_store.search(req.question, req.top_k)
    context = [h["text"] for h in hits]
    answer = llm.generate(req.question, context)

    return QueryResponse(
        answer=answer,
        sources=[
            SearchResultSchema(
                text=h["text"], score=h["score"], 
                chunk_id=h["chunk_id"], document_name=h["document_name"]
            ) for h in hits
        ]
    )