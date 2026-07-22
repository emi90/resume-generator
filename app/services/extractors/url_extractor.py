from readability import Document
from bs4 import BeautifulSoup
import httpx

from app.core.config import Settings
from app.services.extractors.types import ExtractionResult


USER_AGENT = "resume-generator/0.1 (+https://local)"


async def fetch_html(url: str, timeout_seconds: float) -> str:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text



def extract_text_from_html(html: str) -> ExtractionResult:
    warnings: list[str] = []

    doc = Document(html)
    title = (doc.short_title() or "").strip()
    summary_html = doc.summary(html_partial=True)

    soup = BeautifulSoup(summary_html, "html.parser")
    text = soup.get_text("\n", strip=True)

    # Heuristic warning when content looks too short or not job-like.
    if len(text) < 250:
        warnings.append("Low-confidence section extraction from URL content.")

    if title:
        text = f"{title}\n\n{text}".strip()

    return ExtractionResult(text=text, warnings=warnings, meta={"parser": "url"})


async def fetch_and_extract_job_text(url: str, settings: Settings) -> ExtractionResult:
    html = await fetch_html(url, settings.request_timeout_seconds)
    return extract_text_from_html(html)
