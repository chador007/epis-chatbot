from typing import List
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

class DocumentProcessor:

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def extract_text(self, pdf_path: str) -> str:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return 
    
    def clean_text(self,text: str) -> str:
        if text is None:
            return ""
        text = str(text)
        text = re.sub(r'[^A-Za-z0-9\s.,;:()\-]', '', text)
        return re.sub(r'\s+', ' ', text).strip()
