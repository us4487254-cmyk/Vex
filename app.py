import os
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Vex Jarvis", version="0.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


def generate_demo_reply(user_message: str) -> str:
    message = user_message.lower().strip()
    now = datetime.now().strftime("%I:%M %p")

    if not message:
        return "I’m ready when you are, sir."

    if "hello" in message or "hi" in message or "hey" in message:
        return "Good to see you. I’m Jarvis, your AI assistant. How may I help today?"

    if "time" in message:
        return f"The current time is {now}."

    if "status" in message or "how are you" in message:
        return "All systems are nominal. I’m online and ready to assist."

    if "weather" in message:
        return "I can’t check live weather without a connected weather API, but I can help you build that integration."

    if "plan" in message or "schedule" in message:
        return "I can help you organize tasks, create priorities, and structure your day. What would you like to plan?"

    if "research" in message:
        return "I can help summarize sources, draft notes, and identify the key ideas from a topic."

    return (
        "I’m here to help. I can answer questions, summarize information, draft plans, "
        "and build an assistant workflow for your project."
    )


@app.get("/")
async def index():
    return FileResponse("templates/index.html")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are Jarvis, a highly capable AI assistant. "
                            "Be concise, helpful, and professional. "
                            "Use a calm, futuristic tone."
                        ),
                    },
                    {"role": "user", "content": message},
                ],
            )
            reply = response.output_text
            return {"reply": reply, "mode": "live"}
        except Exception as exc:  # pragma: no cover
            return {
                "reply": f"Live model failed, so I switched to demo mode. {generate_demo_reply(message)} Error: {exc}",
                "mode": "demo",
            }

    return {"reply": generate_demo_reply(message), "mode": "demo"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
