from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.chat_router import router


app = FastAPI(title="ePIS RAG Chatbot")

# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "https://my-cool-app.com",
#     "https://api.my-cool-app.com",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}