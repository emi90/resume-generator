from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)



def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"



def test_ingest_with_text_inputs() -> None:
    resume_text = (
        "Experienced software engineer with strong backend and API design skills. "
        "Delivered microservices, integration layers, monitoring pipelines, and reliability improvements "
        "across multiple production systems."
    )
    job_text = (
        "Looking for a backend engineer to build Python APIs, scale services, improve reliability, "
        "and collaborate with product and platform teams to deliver secure, high-quality releases."
    )

    payload = {
        "keyword_level": "7",
        "output_format": "markdown",
        "resume_text": resume_text,
        "job_text": job_text,
    }

    response = client.post("/api/v1/ingest", data=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["source_metadata"]["resume_source"] == "text"
    assert body["source_metadata"]["job_source"] == "text"



def test_ingest_requires_inputs() -> None:
    payload = {
        "keyword_level": "5",
        "output_format": "text",
    }

    response = client.post("/api/v1/ingest", data=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "INVALID_INPUT"
