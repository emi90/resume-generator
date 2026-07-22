from fastapi import FastAPI

from app.api.routes.ingest import router as ingest_router
from app.core.errors import add_exception_handlers


app = FastAPI(title="Resume Generator API", version="0.1.0")

add_exception_handlers(app)
app.include_router(ingest_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
