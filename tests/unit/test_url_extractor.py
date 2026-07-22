import pytest

from app.core.config import Settings
from app.core.errors import ApiError
from app.services.extractors.types import ExtractionResult
from app.services.extractors.url_extractor import extract_text_from_html
from app.services.ingestion.job_parser import parse_job_url
from app.services.validators.url_validator import validate_public_http_url



def test_url_validator_blocks_localhost() -> None:
    with pytest.raises(ApiError):
        validate_public_http_url("http://localhost/job")



def test_extract_text_from_html() -> None:
    html = """
    <html>
      <head><title>Senior Engineer</title></head>
      <body>
        <main>
          <h1>Senior Backend Engineer</h1>
          <p>Responsibilities include APIs and distributed systems.</p>
        </main>
      </body>
    </html>
    """

    result = extract_text_from_html(html)
    assert "Senior" in result.text


@pytest.mark.asyncio
async def test_parse_job_url_uses_extractor(monkeypatch) -> None:
    async def fake_fetch(_url: str, _settings: Settings) -> ExtractionResult:
        return ExtractionResult(text="Senior Engineer role with Python and API delivery.")

    monkeypatch.setattr("app.services.ingestion.job_parser.fetch_and_extract_job_text", fake_fetch)
    monkeypatch.setattr("app.services.validators.url_validator.socket.getaddrinfo", lambda *_: [(None, None, None, None, ("93.184.216.34", 80))])

    text, warnings, safe_url = await parse_job_url(
        "https://example.com/job",
        Settings(min_job_text_chars=10),
    )
    assert "Senior Engineer" in text
    assert warnings == []
    assert safe_url == "https://example.com/job"
