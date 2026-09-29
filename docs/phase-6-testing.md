# Phase 6 - Project Testing
Run `pytest -q`.

Manual test checklist:
- Home page loads.
- Invalid required form fields are rejected by browser/backend validation.
- A valid user creates a 7-day plan.
- Result page displays plan and tip.
- Feedback page accepts changes.
- Updated plan appears after feedback.
- Admin key opens `/view-all-users`.
- `/health` returns status `ok`.
- `/docs` opens Swagger UI.