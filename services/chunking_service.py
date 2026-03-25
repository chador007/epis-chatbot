# services/chunking_service.py
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from config import settings


class ChunkingService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
            api_key=settings.GOOGLE_API_KEY
        )

    def chunk(self, text: str) -> List[str]:
        prompt = f"""Split the following text into semantically meaningful chunks.
Each chunk should be a coherent, self-contained unit of information.
Return ONLY a valid JSON array of strings — no explanation, no markdown.

Example output format:
["chunk one text here", "chunk two text here", "chunk three text here"]

Text to chunk:
{text}"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            return json.loads(content)
        except json.JSONDecodeError:
            return [text]
        except Exception as e:
            raise RuntimeError(f"LLM chunking failed: {e}") from e