import os
from fastapi import FastAPI
from app.routes.chatbot_route import router as chat_router
from fastapi.responses import FileResponse
from app.routes.system_prompt import router as system_prompt_router

app = FastAPI(tittle="My All Works API")
app.include_router(chat_router, prefix="/first", tags=["chat"])
app.include_router(system_prompt_router, prefix="/second", tags=["system_prompt"])

@app.get("/")
async def root():
    return {"message": "Welcome to My All Works API"}
