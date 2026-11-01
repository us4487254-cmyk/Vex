import os
from datetime import datetime
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from config import Config

app = FastAPI(title="Vex Jarvis", version="0.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

def generate_demo_reply(user_message: str) -> str:
    message = user_message.lower().strip()
    now = datetime.now().strftime("%I:%M %p")

    if not message:
        return "I'm ready when you are, sir."

    if "hello" in message or "hi" in message or "hey" in message:
        return "Good to see you, I'm Jarvis, your AI assistant. How may I help today?"

    if "time" in message:
        return f"The current time is {now}."

    if "status" in message or "how are you" in message:
        return "All systems are nominal. I'm online and ready to assist."

    if "weather" in message:
        return "I can't live weather without a connected weather API, but I can help you analyze weather data or plan ahead."

    if "plan" in message or "schedule" in message:
        return "To optimize your daily schedule, create priorities, and structure your day, what would you like to tackle first?"

    return f"I hear you. To automate this task, you can connect an API or expand my knowledge base in config.py."

@app.get("/")
def read_root():
    return FileResponse("templates/index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    api_key = Config.OPENAI_API_KEY

    if not api_key:
        reply = generate_demo_reply(message)
        return {"reply": reply, "mode": "demo"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a highly capable AI assistant. "
                        "You should be concise, helpful, and professional. "
                        "Use a calm, futuristic tone."
                    ),
                },
                {"role": "user", "content": message},
            ],
        )
        reply = response.choices[0].message.content
        return {"reply": reply, "mode": "live"}
    except Exception as exc:  # pragma: no cover
        reply = f"Live model failed, so I switched to demo mode. {generate_demo_reply(message)}"
        return {"reply": reply, "mode": "demo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
