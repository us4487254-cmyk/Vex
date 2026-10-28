# Vex Jarvis

A small Jarvis-inspired AI assistant starter built with Python + FastAPI.

Features:
- Voice-enabled chat UI in the browser
- Dark futuristic dashboard styling
- Works in demo mode without an API key
- Optional OpenAI integration via `OPENAI_API_KEY`

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open the app in your browser:
   ```text
   http://localhost:8000/
   ```

## Optional live AI mode

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

Then run the app with the environment loaded or export the variable:

```bash
export OPENAI_API_KEY="your-key-here"
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Notes

This project is intentionally lightweight and meant to be a starting point for a more advanced AI assistant, automation hub, or personal dashboard.
