from app.core.errors import ApiError
from app.services.extractors.docx_extractor import extract_docx
from app.services.extractors.markdown_extractor import extract_markdown
from app.services.extractors.pdf_extractor import extract_pdf
from app.services.extractors.text_extractor import extract_text
from app.services.extractors.types import ExtractionResult
from app.services.ingestion.normalizer import normalize_text
from app.services.validators.input_validator import validate_min_text_length
from app.utils.mime import get_extension


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}



def parse_resume_file(filename: str, file_bytes: bytes) -> tuple[str, list[str], str]:
    extension = get_extension(filename)
    if extension not in SUPPORTED_EXTENSIONS:
        raise ApiError(
            400,
            "UNSUPPORTED_RESUME_FILE_TYPE",
            "Unsupported resume file type. Allowed: .pdf, .docx, .txt, .md",
            {"extension": extension},
        )

    result: ExtractionResult
    if extension == ".pdf":
        result = extract_pdf(file_bytes)
    elif extension == ".docx":
        result = extract_docx(file_bytes)
    elif extension == ".txt":
        result = extract_text(file_bytes)
    else:
        result = extract_markdown(file_bytes)

    normalized = normalize_text(result.text)
    return normalized, result.warnings, extension.lstrip(".")



def parse_resume_text(resume_text: str, min_chars: int) -> tuple[str, list[str]]:
    normalized = normalize_text(resume_text)
    validate_min_text_length(normalized, min_chars, "resume_text")
    return normalized, []
