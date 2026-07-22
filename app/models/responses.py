from pydantic import BaseModel, Field

from app.models.enums import JobSource, OutputFormat, ResumeSource


class SourceMetadata(BaseModel):
    resume_source: ResumeSource
    resume_file_type: str | None = None
    job_source: JobSource
    job_url: str | None = None


class IngestResponse(BaseModel):
    resume_text_normalized: str
    job_text_normalized: str
    keyword_level: int = Field(ge=1, le=10)
    output_format: OutputFormat
    source_metadata: SourceMetadata
    warnings: list[str] = Field(default_factory=list)
