import pytest

from app.core.errors import ApiError
from app.services.validators.input_validator import (
    validate_input_combination,
    validate_max_upload_size,
    validate_min_text_length,
)



def test_requires_single_resume_source() -> None:
    with pytest.raises(ApiError) as exc:
        validate_input_combination(
            has_resume_file=False,
            resume_text=None,
            job_text="job text",
            job_url=None,
        )
    assert exc.value.status_code == 422



def test_rejects_multiple_resume_sources() -> None:
    with pytest.raises(ApiError):
        validate_input_combination(
            has_resume_file=True,
            resume_text="already here",
            job_text="job text",
            job_url=None,
        )



def test_rejects_multiple_job_sources() -> None:
    with pytest.raises(ApiError):
        validate_input_combination(
            has_resume_file=False,
            resume_text="resume",
            job_text="job",
            job_url="https://example.com/job",
        )



def test_upload_size_limit() -> None:
    with pytest.raises(ApiError) as exc:
        validate_max_upload_size(file_size_bytes=2 * 1024 * 1024, max_upload_mb=1)
    assert exc.value.status_code == 413



def test_text_min_length() -> None:
    with pytest.raises(ApiError):
        validate_min_text_length("short", min_chars=10, field_name="resume_text")
