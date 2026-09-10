# Agent Instructions

- Treat `_docs/specs.md` and `openapi.yaml` as the product and API sources of truth.
- Keep all backend access centralized in `frontend/src/api.js`.
- Use FastAPI, SQLAlchemy, SQLite, and uv for the backend.
- Write or update tests whenever behavior changes.
- Keep the implementation small and within the documented non-goals.
- Run backend tests and frontend build before committing.

