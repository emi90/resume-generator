from app.services.extractors.types import ExtractionResult



def extract_text(file_bytes: bytes) -> ExtractionResult:
    warnings: list[str] = []
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1", errors="replace")
        warnings.append("Decoded text using latin-1 fallback.")
    return ExtractionResult(text=text, warnings=warnings, meta={"parser": "text"})
