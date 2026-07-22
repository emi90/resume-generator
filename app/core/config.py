import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    max_upload_mb: int = 8
    request_timeout_seconds: float = 10.0
    min_job_text_chars: int = 120
    min_resume_text_chars: int = 120
    log_level: str = "INFO"



def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default



def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default



def get_settings() -> Settings:
    return Settings(
        max_upload_mb=_get_int("MAX_UPLOAD_MB", 8),
        request_timeout_seconds=_get_float("REQUEST_TIMEOUT_SECONDS", 10.0),
        min_job_text_chars=_get_int("MIN_JOB_TEXT_CHARS", 120),
        min_resume_text_chars=_get_int("MIN_RESUME_TEXT_CHARS", 120),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
