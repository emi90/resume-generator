from fastapi import APIRouter, File, Form, UploadFile

from app.core.config import get_settings
from app.models.enums import JobSource, OutputFormat, ResumeSource
from app.models.responses import IngestResponse, SourceMetadata
from app.services.ingestion.job_parser import parse_job_text, parse_job_url
from app.services.ingestion.resume_parser import parse_resume_file, parse_resume_text
from app.services.validators.input_validator import validate_input_combination, validate_max_upload_size


router = APIRouter(prefix="/api/v1", tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    keyword_level: int = Form(..., ge=1, le=10),
    output_format: OutputFormat = Form(...),
    resume_file: UploadFile | None = File(default=None),
    resume_text: str | None = Form(default=None),
    job_text: str | None = Form(default=None),
    job_url: str | None = Form(default=None),
) -> IngestResponse:
    settings = get_settings()
    validate_input_combination(
        has_resume_file=resume_file is not None,
        resume_text=resume_text,
        job_text=job_text,
        job_url=job_url,
    )

    warnings: list[str] = []

    if resume_file is not None:
        file_bytes = await resume_file.read()
        validate_max_upload_size(len(file_bytes), settings.max_upload_mb)
        resume_normalized, resume_warnings, file_type = parse_resume_file(
            resume_file.filename or "resume",
            file_bytes,
        )
        warnings.extend(resume_warnings)
        resume_source = ResumeSource.FILE
    else:
        resume_normalized, resume_warnings = parse_resume_text(
            resume_text or "",
            settings.min_resume_text_chars,
        )
        warnings.extend(resume_warnings)
        file_type = None
        resume_source = ResumeSource.TEXT

    if job_text is not None and job_text.strip():
        job_normalized, job_warnings = await parse_job_text(job_text, settings.min_job_text_chars)
        warnings.extend(job_warnings)
        job_source = JobSource.TEXT
        selected_job_url = None
    else:
        job_normalized, job_warnings, selected_job_url = await parse_job_url(job_url or "", settings)
        warnings.extend(job_warnings)
        job_source = JobSource.URL

    return IngestResponse(
        resume_text_normalized=resume_normalized,
        job_text_normalized=job_normalized,
        keyword_level=keyword_level,
        output_format=output_format,
        source_metadata=SourceMetadata(
            resume_source=resume_source,
            resume_file_type=file_type,
            job_source=job_source,
            job_url=selected_job_url,
        ),
        warnings=warnings,
    )
