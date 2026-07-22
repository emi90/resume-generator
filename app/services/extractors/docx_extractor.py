import io

from docx import Document

from app.services.extractors.types import ExtractionResult



def extract_docx(file_bytes: bytes) -> ExtractionResult:
    document = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text and p.text.strip()]
    text = "\n".join(paragraphs).strip()
    return ExtractionResult(text=text, warnings=[], meta={"parser": "docx"})
