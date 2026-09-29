# FitBuddy - AI Fitness Plan Generator

A complete FastAPI + Jinja2 + SQLite implementation of the SmartBridge FitBuddy project.

## Features
- User form: name, user ID, age, weight, goal, intensity
- 7-day AI workout generation
- Nutrition/recovery tip
- Feedback-based plan regeneration
- SQLite persistence with SQLAlchemy
- Admin/local all-users dashboard
- REST endpoints and Swagger docs
- Responsive HTML/CSS frontend
- Mock/demo mode when no Gemini key is configured
- Automated pytest tests

## Project structure
```text
fitbuddy/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── services/
├── templates/
├── static/
├── tests/
├── docs/
├── data/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code
1. Install Python 3.11+ and VS Code.
2. Open this folder.
3. Terminal -> New Terminal.
4. Windows: `py -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
5. macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
6. `pip install -r requirements.txt`
7. Copy `.env.example` to `.env`.
8. Put your Gemini API key into `GEMINI_API_KEY` for real AI generation.
9. Run `uvicorn app.main:app --reload`
10. Open `http://127.0.0.1:8000`
11. Swagger: `http://127.0.0.1:8000/docs`

## AI modes
`AI_MODE=auto` uses Gemini if a key exists; otherwise it uses a local deterministic demo generator.
`AI_MODE=gemini` requires a Gemini key.
`AI_MODE=mock` is intended for tests.

The source document names Gemini 1.5 Pro and Gemini Flash. Those are historical model references, so the implementation keeps the same Pro/Flash architecture but uses configurable current model IDs. Defaults are `gemini-3.8-flash` for workout generation and `gemini-3.5-flash-lite` for the fast tip path.

## Admin
Open `/view-all-users`, enter the `ADMIN_KEY` value from `.env`. The dashboard is intentionally simple for the educational/local project; production deployments should use proper authentication and authorization.

## Testing
Run `pytest -q`.

## Safety
This is a general wellness educational application, not medical care. AI output should not be used to diagnose illness or replace a qualified professional.
