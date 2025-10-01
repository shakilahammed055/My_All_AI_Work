import os
from fastapi import FastAPI
from app.routes.chatbot_route import router as chat_router
from fastapi.responses import FileResponse

app = FastAPI(tittle="My All Works API")
app.include_router(chat_router, prefix="/first", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to My All Works API"}
