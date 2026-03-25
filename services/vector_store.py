import uuid
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


class VectorStore:

    def __init__(self, host, port, collection_name, embedding_model):

        self.collection_name = collection_name

        self.client = QdrantClient(host=host, port=port)

        self.embedder = SentenceTransformer(embedding_model)

        self.vector_size = self.embedder.get_sentence_embedding_dimension()

        self._ensure_collection()

    def _ensure_collection(self):

        collections = self.client.get_collections().collections

        if not any(c.name == self.collection_name for c in collections):

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def embed(self, text: str, is_query: bool = False):
        if is_query:
            text = f"Represent this sentence for searching relevant passages: {text}"
        return self.embedder.encode(text).tolist()

    def add(self, chunks: List[str], metadata: Dict[str, Any]):

        points = []

        for i, chunk in enumerate(chunks):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=self.embed(chunk),          # no prefix for stored chunks
                    payload={
                        "text": chunk,
                        "chunk_id": i,
                        "document_name": metadata["document_name"]
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    def search(self, query: str, k: int = 5):

        vector = self.embed(query, is_query=True)      # prefix applied for queries

        hits = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=k
        ).points

        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "chunk_id": hit.payload["chunk_id"],
                "document_name": hit.payload["document_name"]
            }
            for hit in hits
        ]