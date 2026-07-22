import httpx

from app.core.config import Settings
from app.core.errors import ApiError
from app.services.extractors.url_extractor import fetch_and_extract_job_text
from app.services.ingestion.normalizer import normalize_text
from app.services.validators.input_validator import validate_min_text_length
from app.services.validators.url_validator import validate_public_http_url


async def parse_job_text(job_text: str, min_chars: int) -> tuple[str, list[str]]:
    normalized = normalize_text(job_text)
    validate_min_text_length(normalized, min_chars, "job_text")
    return normalized, []


async def parse_job_url(job_url: str, settings: Settings) -> tuple[str, list[str], str]:
    safe_url = validate_public_http_url(job_url)

    try:
        result = await fetch_and_extract_job_text(safe_url, settings)
    except httpx.HTTPStatusError as exc:
        raise ApiError(422, "JOB_URL_FETCH_FAILED", "Job URL returned an error response.") from exc
    except httpx.HTTPError as exc:
        raise ApiError(422, "JOB_URL_FETCH_FAILED", "Unable to fetch job URL.") from exc

    normalized = normalize_text(result.text)
    validate_min_text_length(normalized, settings.min_job_text_chars, "job_text")
    return normalized, result.warnings, safe_url
