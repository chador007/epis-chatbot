# services/llm_service.py
from typing import List
from openai import OpenAI
import json
from config import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class LLMService:
    def __init__(self, base_url: str, model: str):
        self.client = OpenAI(base_url=base_url, api_key="dummy")
        self.model = model

    def generate(self, query: str, context: List[str]) -> str:
        context_text = "\n\n".join(context)
        system_prompt = "You are an EPIS assistant helping doctors navigate the system. Use only provided documentation context."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:{query}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content