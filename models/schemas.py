from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class SearchResultSchema(BaseModel):
    text: str
    score: float
    chunk_id: int
    document_name: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SearchResultSchema]  


