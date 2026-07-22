import io

from pypdf import PdfReader

from app.services.extractors.types import ExtractionResult



def extract_pdf(file_bytes: bytes) -> ExtractionResult:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages: list[str] = []
    warnings: list[str] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text.strip():
            warnings.append(f"Page {index} had low extraction quality.")
        pages.append(text)

    extracted = "\n".join(pages).strip()
    return ExtractionResult(
        text=extracted,
        warnings=warnings,
        meta={"parser": "pdf", "pages": len(reader.pages)},
    )
