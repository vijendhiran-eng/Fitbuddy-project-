# Phase 3 - Project Design
Frontend: Jinja2 templates + CSS/JavaScript.
Backend: FastAPI routes and Pydantic validation.
AI layer: Google Gemini through the `google-genai` SDK.
Data layer: SQLAlchemy ORM + SQLite.

Flow: form -> validation -> Gemini workout + tip -> database -> result page -> feedback -> revised plan -> database.