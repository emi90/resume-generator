from pydantic import BaseModel, Field

from app.models.enums import OutputFormat


class IngestRequestData(BaseModel):
    resume_text: str
    job_text: str
    keyword_level: int = Field(ge=1, le=10)
    output_format: OutputFormat
