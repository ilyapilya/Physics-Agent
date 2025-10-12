# Copilot Instructions for Physics-Agent

## Project Overview
- **Physics-Agent** is a multi-component system for physics workflow automation using LLMs (Google Gemini), FastAPI, SQLAlchemy (with SQLite), and a React.js frontend (Vite + TypeScript).
- The backend (`physics-gemini/`) exposes API endpoints, manages database operations, and handles LLM prompting.
- The frontend (`react-ui/`) is a Vite-based React app for workflow management.
- Containerization is supported via Docker; see `Dockerfile` in both main and frontend directories.

## Key Directories & Files
- `physics-gemini/routes/api.py`: Main FastAPI entrypoint. Run with `python api.py` from this directory.
- `physics-gemini/services/database.py`: SQLAlchemy DB logic. Uses SQLite, auto-initialized on app start.
- `physics-gemini/prompting/promptLoader.py` & `prompts.yaml`: Loads and manages LLM prompt templates.
- `react-ui/`: Frontend app. Entry: `src/main.tsx`, config: `vite.config.ts`, lint: `eslint.config.js`.
- `tests/`: Contains Python and shell-based tests for backend and agent logic.
- `.env`: Required for backend. Must set `GEMINI_API_KEY`.

## Developer Workflows
- **Backend**: Activate Python venv, install dependencies from `requirements.txt` or README, run `python physics-gemini/routes/api.py`.
- **Frontend**: Use Vite commands (`npm install`, `npm run dev`) in `react-ui/`.
- **Testing**: Run `pytest tests/` for backend. Shell scripts in `tests/` for agent tests.
- **Formatting**: Use `black .` for Python code. Lint with `pylint` or ESLint for frontend.
- **Docker**: Build containers using provided `Dockerfile` and `docker-compose.yml`.

## Patterns & Conventions
- **Prompt Management**: Prompts are YAML-based (`physics-gemini/prompting/prompts.yaml`) and loaded via `promptLoader.py`.
- **Database**: All DB schema and logic in `physics-gemini/services/database.py` and `database/`.
- **Environment**: `.env` file required for API key. Do not commit secrets.
- **Testing**: Python tests in `tests/gemini-func-test.py`, shell tests for agent logic.
- **Frontend**: TypeScript, Vite, and ESLint. See `react-ui/README.md` for linting and build details.

## Integration Points
- **LLM**: Google Gemini API via `google-generativeai` package. Key in `.env`.
- **API**: FastAPI endpoints in `physics-gemini/routes/api.py`.
- **Database**: SQLAlchemy ORM, SQLite backend.
- **Frontend**: Communicates with backend via REST endpoints.

## Examples
- To run backend: `python physics-gemini/routes/api.py`
- To run tests: `pytest tests/`
- To run frontend: `cd react-ui && npm install && npm run dev`
- To format Python: `black .`

## Additional Notes
- All major logic is in `physics-gemini/`. Frontend is in `react-ui/`.
- Database is auto-initialized; no manual migration needed for SQLite.
- Prompts are managed via YAML for easy editing and extension.
- For new agents, review `README.md` and this file for workflow and conventions.
