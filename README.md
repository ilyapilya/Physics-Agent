# Physics Agent Wrapper (made with Gemini)

## Components:
- Google Gemini API - Utilized for LLM prompting
- FastAPI - Backend API Endpoint Integration
- MySQL / SQLAlchemy - Python SQL wrapper for easy database integration
- React.js Frontend - Workflow Management (TODO)
- UnitTests - CI/CD and Stability Checks
- Docker - Project Containerization

## Installation Guide

### 1. Set Up Virtual Environment
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS
```

### 2. Install Dependencies
```bash
# Core dependencies
pip install fastapi uvicorn google-generativeai python-dotenv pydantic

# Database dependencies
pip install sqlalchemy

# Development dependencies
pip install pytest pyyaml
```

### 3. Environment Setup
Create a `.env` file in the root directory with:
```
GEMINI_API_KEY=your_api_key_here
```

### 4. Database Setup
The application uses SQLAlchemy with SQLite. The database will be automatically initialized when running the application.

### 5. Running the Application
```bash
# From the physics-gemini/routes directory
python api.py
```

### Optional: Development Tools
```bash
# Install development dependencies
pip install black pylint pytest-cov

# Format code
black .

# Run tests
pytest tests/
```
