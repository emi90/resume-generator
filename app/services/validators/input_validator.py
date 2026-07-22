from app.core.errors import ApiError



def validate_input_combination(
    *,
    has_resume_file: bool,
    resume_text: str | None,
    job_text: str | None,
    job_url: str | None,
) -> None:
    has_resume_text = bool((resume_text or "").strip())
    has_job_text = bool((job_text or "").strip())
    has_job_url = bool((job_url or "").strip())

    if not has_resume_file and not has_resume_text:
        raise ApiError(
            422,
            "INVALID_INPUT",
            "Provide either resume_file or resume_text.",
            {"field": "resume_text"},
        )

    if has_resume_file and has_resume_text:
        raise ApiError(
            422,
            "INVALID_INPUT",
            "Provide only one of resume_file or resume_text.",
            {"field": "resume_file"},
        )

    if not has_job_text and not has_job_url:
        raise ApiError(
            422,
            "INVALID_INPUT",
            "Provide either job_text or job_url.",
            {"field": "job_text"},
        )

    if has_job_text and has_job_url:
        raise ApiError(
            422,
            "INVALID_INPUT",
            "Provide only one of job_text or job_url.",
            {"field": "job_text"},
        )



def validate_max_upload_size(file_size_bytes: int, max_upload_mb: int) -> None:
    max_bytes = max_upload_mb * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise ApiError(
            413,
            "UPLOAD_TOO_LARGE",
            f"Resume file exceeds {max_upload_mb} MB size limit.",
            {"max_upload_mb": max_upload_mb},
        )



def validate_min_text_length(text: str, min_chars: int, field_name: str) -> None:
    if len(text.strip()) < min_chars:
        raise ApiError(
            422,
            "CONTENT_TOO_SHORT",
            f"{field_name} must be at least {min_chars} characters after parsing.",
            {"field": field_name, "min_chars": min_chars},
        )
