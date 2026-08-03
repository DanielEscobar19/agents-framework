import uvicorn

from agents_framework.api.server import (
    app,
)  # noqa: F401 — imported for uvicorn string reference

if __name__ == "__main__":
    uvicorn.run(
        "agents_framework.api.server:app", host="0.0.0.0", port=8000, reload=True
    )
