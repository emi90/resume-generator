from app.services.extractors.types import ExtractionResult
from app.services.extractors.text_extractor import extract_text



def extract_markdown(file_bytes: bytes) -> ExtractionResult:
    result = extract_text(file_bytes)
    result.meta["parser"] = "markdown"
    return result
