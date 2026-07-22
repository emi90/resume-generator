# Resume Generator

## Project Description

Resume Generator is a backend-first project that ingests a resume and a job description, validates and normalizes both inputs, and prepares clean structured data for later LLM tailoring.

The implementation currently covers Phase 1 (Core Backend) only.

## Implemented API

### Health

- Method: GET
- Path: /health
- Purpose: basic service liveness check

### Ingest

- Method: POST
- Path: /api/v1/ingest
- Content type: multipart/form-data
- Purpose: validate and parse resume + job description input into normalized text

Accepted fields:

- keyword_level (required, integer 1 through 10)
- output_format (required, markdown or text)
- resume_file (optional, mutually exclusive with resume_text)
- resume_text (optional, mutually exclusive with resume_file)
- job_text (optional, mutually exclusive with job_url)
- job_url (optional, mutually exclusive with job_text)

Response includes:

- normalized resume text
- normalized job description text
- source metadata
- warnings from parsers/extractors

## Validation and Safety Behavior

- Enforces one resume source and one job source
- Enforces supported resume file types
- Enforces upload size limits
- Enforces minimum parsed text length
- URL validation includes scheme and host checks
- URL resolution blocks local/private/internal network targets

## Tech Stack (Implemented)

- Python 3.14
- FastAPI
- Pydantic
- HTTPX
- pypdf
- python-docx
- readability-lxml
- beautifulsoup4
- pytest

## Run Locally

From repository root:

1. Install dependencies

   uv sync

2. Start API server

   uv run uvicorn app.main:app --reload

3. Open API docs

   http://127.0.0.1:8000/docs

## Run Tests

Run all unit tests:

uv run pytest tests/unit -q

Run parser tests only:

uv run pytest tests/unit/test_file_parsers.py -q

## Fixture Notes

Real fixture files are used in parser tests:

- tests/fixtures/sample_resume.pdf
- tests/fixtures/sample_resume.docx
- tests/fixtures/sample_bad_resume.xlsx

The XLSX fixture is intentionally unsupported and is tested to confirm graceful rejection.

## Next Planned Step

Phase 2 is next: LLM tailoring engine integration on top of the normalized ingestion contract produced by the current backend.
